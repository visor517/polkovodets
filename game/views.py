from datetime import timedelta

from django.db.models import Q

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.response import Response

from game import exceptions as err
from game import serializers
from game.army import UNIT_STATS
from game.forms import CreateGameForm
from game.models import Army, Game, Unit


def lobby_view(request):
    """Лобби — главная страница"""

    if request.user.is_authenticated:
        my_games_filter = Q(player1=request.user) | Q(player2=request.user)
        context = {
            "my_games": Game.objects.filter(my_games_filter).order_by("-created_at"),
            "waiting_games": Game.objects.filter(status="waiting").exclude(my_games_filter).order_by("-created_at"),
        }
    
    else:
        context = {
            "waiting_games": Game.objects.filter(status="waiting").order_by("-created_at"),
        }

    return render(request, "lobby.html", context)


@login_required
def create_game_view(request):
    """Создание игры"""

    if request.method == "GET":
        # FIXME: Временно удаляем игры старше 24 часов
        Game.objects.filter(created_at__lt=timezone.now() - timedelta(hours=24)).delete()

        return render(request, "game/create_game.html", {"form": CreateGameForm()})

    elif request.method == "POST":
        form = CreateGameForm(request.POST)
        if not form.is_valid():
            return render(request, "game/create_game.html", {"form": form})

        data = form.cleaned_data

        player2 = data.get("player2")
        status = data.get("status")

        # Определяем, кто какими войсками играет
        first_side = data["player1_side"] if data["first_turn"] == "player1" else data["player2_side"]
        second_side = data["player2_side"] if data["first_turn"] == "player1" else data["player1_side"]

        # Создаём игру
        game = Game.objects.create(
            name=data["name"],
            player1=request.user,
            player2=player2,
            status=status,
            player1_side=data["player1_side"],
            player2_side=data["player2_side"],
            is_player1_first=(data["first_turn"] == "player1"),
            player1_mr=data["player1_mr"],
            player2_mr=data["player2_mr"],
            move_number=1
        )

        # Начальная расстановка юнитов временно
        initial_units = [
            # Русские (левая сторона)
            {"unit_type": "infantry", "army": Army.RUSSIAN, "x": 1, "y": 2},
            {"unit_type": "infantry", "army": Army.RUSSIAN, "x": 1, "y": 3},
            {"unit_type": "infantry", "army": Army.RUSSIAN, "x": 1, "y": 4},
            {"unit_type": "infantry", "army": Army.RUSSIAN, "x": 2, "y": 2},
            {"unit_type": "infantry", "army": Army.RUSSIAN, "x": 2, "y": 3},
            {"unit_type": "infantry", "army": Army.RUSSIAN, "x": 2, "y": 4},
            {"unit_type": "grenadier", "army": Army.RUSSIAN, "x": 1, "y": 5},
            {"unit_type": "grenadier", "army": Army.RUSSIAN, "x": 2, "y": 5},
            {"unit_type": "huntsman", "army": Army.RUSSIAN, "x": 2, "y": 7},
            {"unit_type": "huntsman", "army": Army.RUSSIAN, "x": 2, "y": 8},
            {"unit_type": "huntsman", "army": Army.RUSSIAN, "x": 2, "y": 9},
            {"unit_type": "huntsman", "army": Army.RUSSIAN, "x": 2, "y": 10},

            {"unit_type": "artillery", "army": Army.RUSSIAN, "x": 3, "y": 5},
            {"unit_type": "artillery", "army": Army.RUSSIAN, "x": 3, "y": 6},

            {"unit_type": "hussar", "army": Army.RUSSIAN, "x": 4, "y": 10},
            {"unit_type": "hussar", "army": Army.RUSSIAN, "x": 4, "y": 11},
            {"unit_type": "cuirassier", "army": Army.RUSSIAN, "x": 4, "y": 1},
            {"unit_type": "cuirassier", "army": Army.RUSSIAN, "x": 4, "y": 2},

            # Французы (правая сторона)
            {"unit_type": "infantry", "army": Army.FRENCH, "x": 14, "y": 2},
            {"unit_type": "infantry", "army": Army.FRENCH, "x": 14, "y": 3},
            {"unit_type": "infantry", "army": Army.FRENCH, "x": 14, "y": 4},
            {"unit_type": "infantry", "army": Army.FRENCH, "x": 14, "y": 5},
            {"unit_type": "infantry", "army": Army.FRENCH, "x": 14, "y": 6},
            {"unit_type": "infantry", "army": Army.FRENCH, "x": 14, "y": 7},
            {"unit_type": "infantry", "army": Army.FRENCH, "x": 14, "y": 8},
            {"unit_type": "huntsman", "army": Army.FRENCH, "x": 13, "y": 2},
            {"unit_type": "huntsman", "army": Army.FRENCH, "x": 13, "y": 3},
            {"unit_type": "huntsman", "army": Army.FRENCH, "x": 13, "y": 4},
            {"unit_type": "huntsman", "army": Army.FRENCH, "x": 13, "y": 5},
            {"unit_type": "huntsman", "army": Army.FRENCH, "x": 13, "y": 6},
            {"unit_type": "huntsman", "army": Army.FRENCH, "x": 13, "y": 7},
            {"unit_type": "huntsman", "army": Army.FRENCH, "x": 13, "y": 8},

            {"unit_type": "artillery", "army": Army.FRENCH, "x": 12, "y": 5},
            {"unit_type": "artillery", "army": Army.FRENCH, "x": 12, "y": 6},

            {"unit_type": "ulan", "army": Army.FRENCH, "x": 14, "y": 10},
            {"unit_type": "ulan", "army": Army.FRENCH, "x": 14, "y": 11},
            {"unit_type": "cuirassier", "army": Army.FRENCH, "x": 13, "y": 10},
            {"unit_type": "cuirassier", "army": Army.FRENCH, "x": 13, "y": 11},
        ]
        for unit_data in initial_units:
            Unit.objects.create(game=game, **unit_data)

        return redirect("game", game_uid=game.uid)


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


@login_required
def join_game_view(request, game_uid):
    game = get_object_or_404(Game, uid=game_uid)

    if game.player2 is not None:
        messages.error(request, "В этой игре уже нет мест")
        return redirect("lobby")

    game.player2 = request.user
    game.status = "active"
    game.save()

    return redirect("game", game_uid=game.uid)


def rules_view(request):
    """Страница правил"""
    return render(request, "rules.html")


@api_view(["POST"])
def end_turn(request):
    """Завершение хода"""
    serializer = serializers.EndTurnSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    game = serializer.validated_data["game"]

    game.move_number += 1
    game.save()

    events = [{
        "type": "round_change",
        "move_number": game.move_number,
        "round_number": game.round_number,
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

    # Уничтожаем врага
    target_cost = UNIT_STATS[target_unit.unit_type]["cost"]
    if target_unit.army == game.player1_side:
        game.player2_score += target_cost
    else:
        game.player1_score += target_cost

    events = [
        {"type": "destroy", "unit_id": target_unit.id},
        {"type": "score_change", "player1_score": game.player1_score, "player2_score": game.player2_score},
    ]
    game.save()
    target_unit.delete()

    # Проверка конца игры
    if winner := game.check_winner():
        events.append({"type": "game_over", "winner": winner})
        return Response({"success": True, "events": events})

    # Если юнит charges перемещаем на место врага
    if UNIT_STATS[unit.unit_type]["charges"]:
        unit.x = to_x
        unit.y = to_y
    unit.last_used_turn = game.move_number
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
    unit.last_used_turn = game.move_number
    unit.save()

    unit_serializer = serializers.UnitSerializer(unit)
    events = [{"type": "unit_updated", "unit": unit_serializer.data}]
    return Response({"success": True, "events": events})
