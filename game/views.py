from datetime import timedelta

from django.db.models import Q

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.response import Response

from game import exceptions as err
from game import serializers
from game.army import UNIT_STATS
from game.models import Army, Game, Unit


def lobby_view(request):
    """Лобби — главная страница"""
    waiting_games = Game.objects.filter(
        status="waiting"
    ).order_by("-created_at")
    
    context = {
        "waiting_games": waiting_games,
    }
    
    if request.user.is_authenticated:
        my_games = Game.objects.filter(
            Q(player1=request.user) | Q(player2=request.user)
        ).exclude(status="finished").order_by("-created_at")[:10]
        context["my_games"] = my_games
    
    return render(request, "lobby.html", context)


def game_view(request, game_uid):
    """Страница игры"""
    game = get_object_or_404(Game, uid=game_uid)
    serializer = serializers.GameSerializer(game)
    
    # Добавляем служебные поля
    context = {
        "game_uid": game_uid,
        "game_data": serializer.data,
        "unit_stats": UNIT_STATS,
    }
    
    return render(request, "game.html", context)


def new_game(request):
    """
    Создание новой игры

    TODO: сделать форму для создания игры
    """

    # FIXME: Временно удаляем игры старше 3 часов
    Game.objects.filter(created_at__lt=timezone.now() - timedelta(hours=3)).delete()

    # Временно привязываем админа
    if not request.user.is_authenticated:
        player1 = User.objects.get(username="admin")
    else:
        player1 = request.user
    
    game = Game.objects.create(
        player1=player1,
        status="waiting",
        first_side=Army.RUSSIAN,
        second_side=Army.FRENCH,
    )
    
    # Начальная расстановка юнитов
    initial_units = [
        {"unit_type": "infantry", "army": Army.RUSSIAN, "x": 1, "y": 4},
        {"unit_type": "infantry", "army": Army.RUSSIAN, "x": 1, "y": 5},
        {"unit_type": "infantry", "army": Army.RUSSIAN, "x": 1, "y": 6},
        {"unit_type": "infantry", "army": Army.RUSSIAN, "x": 1, "y": 7},
        {"unit_type": "infantry", "army": Army.RUSSIAN, "x": 2, "y": 4},
        {"unit_type": "infantry", "army": Army.RUSSIAN, "x": 2, "y": 5},
        {"unit_type": "infantry", "army": Army.RUSSIAN, "x": 2, "y": 6},
        {"unit_type": "infantry", "army": Army.RUSSIAN, "x": 2, "y": 7},
        {"unit_type": "artillery", "army": Army.RUSSIAN, "x": 3, "y": 5},
        {"unit_type": "artillery", "army": Army.RUSSIAN, "x": 3, "y": 6},
        {"unit_type": "cuirassier", "army": Army.RUSSIAN, "x": 2, "y": 1},
        {"unit_type": "cuirassier", "army": Army.RUSSIAN, "x": 2, "y": 2},
        {"unit_type": "dragoon", "army": Army.RUSSIAN, "x": 2, "y": 9},
        {"unit_type": "dragoon", "army": Army.RUSSIAN, "x": 2, "y": 10},

        {"unit_type": "infantry", "army": Army.FRENCH, "x": 10, "y": 4},
        {"unit_type": "infantry", "army": Army.FRENCH, "x": 10, "y": 5},
        {"unit_type": "infantry", "army": Army.FRENCH, "x": 10, "y": 6},
        {"unit_type": "infantry", "army": Army.FRENCH, "x": 10, "y": 7},
        {"unit_type": "infantry", "army": Army.FRENCH, "x": 9, "y": 4},
        {"unit_type": "infantry", "army": Army.FRENCH, "x": 9, "y": 5},
        {"unit_type": "infantry", "army": Army.FRENCH, "x": 9, "y": 6},
        {"unit_type": "infantry", "army": Army.FRENCH, "x": 9, "y": 7},
        {"unit_type": "horse_artillery", "army": Army.FRENCH, "x": 8, "y": 5},
        {"unit_type": "artillery", "army": Army.FRENCH, "x": 8, "y": 6},
        {"unit_type": "cuirassier", "army": Army.FRENCH, "x": 9, "y": 1},
        {"unit_type": "cuirassier", "army": Army.FRENCH, "x": 9, "y": 2},
        {"unit_type": "hussar", "army": Army.FRENCH, "x": 9, "y": 9},
        {"unit_type": "hussar", "army": Army.FRENCH, "x": 9, "y": 10},
    ]
    for unit_data in initial_units:
        Unit.objects.create(game=game, **unit_data)
    
    return redirect("game", game_uid=game.uid)


@api_view(["POST"])
def end_turn(request):
    """Завершение хода"""
    serializer = serializers.EndTurnSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    game = serializer.validated_data["game"]

    game.turn_number += 1
    game.save()

    events = [{
        "type": "turn_change",
        "turn_number": game.turn_number,
        "active_side": game.active_side,
    }]
    return Response({
        "success": True,
        "events": events,
    })


@api_view(["POST"])
def make_attack(request):
    serializer = serializers.UnitActionSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    game = serializer.validated_data["game"]
    unit = serializer.validated_data["unit"]
    to_x = serializer.validated_data["to_x"]
    to_y = serializer.validated_data["to_y"]

    dx = to_x - unit.x
    dy = to_y - unit.y

    # Определяем направление и дальность
    is_diag = abs(dx) == abs(dy)
    is_cross = dx == 0 or dy == 0

    if not (is_cross or is_diag):
        raise err.InvalidDirection

    if is_cross:
        max_range = UNIT_STATS[unit.unit_type]["attack"]["cross"]
        step_x = 0 if dx == 0 else (1 if dx > 0 else -1)
        step_y = 0 if dy == 0 else (1 if dy > 0 else -1)
    else:  # is_diag
        max_range = UNIT_STATS[unit.unit_type]["attack"]["diag"]
        step_x = 1 if dx > 0 else -1
        step_y = 1 if dy > 0 else -1

    distance = max(abs(dx), abs(dy))

    if distance > max_range:
        raise err.OutOfRange

    # Проверяем путь до цели (не включая цель)
    for step in range(1, distance):
        check_x = unit.x + step_x * step
        check_y = unit.y + step_y * step
        if Unit.objects.filter(game=game, x=check_x, y=check_y).exists():
            raise err.PathBlocked

    # Проверяем цель
    target_unit = Unit.objects.filter(game=game, x=to_x, y=to_y).first()
    if not target_unit or target_unit.army == unit.army:
        return err.InvalidTarget

    events = []

    # Уничтожаем врага
    events.append({"type": "destroy", "unit_id": target_unit.id})
    target_unit.delete()

    # Проверка конца игры
    if winner := game.check_winner():
        events.append({"type": "game_over", "winner": winner})
        return Response({"success": True, "events": events})

    # Если юнит charges перемещаем на место врага
    if UNIT_STATS[unit.unit_type]["charges"]:
        unit.x = to_x
        unit.y = to_y
    unit.last_used_turn = game.turn_number
    unit.save()
    unit_serializer = serializers.UnitSerializer(unit)
    events.append({"type": "unit_updated", "unit": unit_serializer.data})

    return Response({"success": True, "events": events})


@api_view(["POST"])
def make_move(request):
    """Обработка хода"""
    serializer = serializers.UnitActionSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    game = serializer.validated_data["game"]
    unit = serializer.validated_data["unit"]
    to_x = serializer.validated_data["to_x"]
    to_y = serializer.validated_data["to_y"]

    dx = to_x - unit.x
    dy = to_y - unit.y

    is_diag = abs(dx) == abs(dy)
    is_cross = dx == 0 or dy == 0

    if not (is_cross or is_diag):
        raise err.InvalidDirection

    if is_cross:
        max_range = UNIT_STATS[unit.unit_type]["move"]["cross"]
        step_x = 0 if dx == 0 else (1 if dx > 0 else -1)
        step_y = 0 if dy == 0 else (1 if dy > 0 else -1)
    else:  # is_diag
        max_range = UNIT_STATS[unit.unit_type]["move"]["diag"]
        step_x = 1 if dx > 0 else -1
        step_y = 1 if dy > 0 else -1

    distance = max(abs(dx), abs(dy))
    if distance > max_range:
        raise err.OutOfRange

    # Проверяем, что путь свободен
    for step in range(1, distance + 1):
        check_x = unit.x + step_x * step
        check_y = unit.y + step_y * step

        if blocker_unit := Unit.objects.filter(game=game, x=check_x, y=check_y).first():
            if blocker_unit.army == unit.army or step < distance:
                raise err.PathBlocked

    unit.x = to_x
    unit.y = to_y
    unit.last_used_turn = game.turn_number
    unit.save()

    unit_serializer = serializers.UnitSerializer(unit)
    events = [{"type": "unit_updated", "unit": unit_serializer.data}]
    return Response({"success": True, "events": events})
