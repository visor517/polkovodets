from datetime import timedelta

from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .army import Army, UNIT_STATS
from .models import Game, Unit
from .serializers import EndTurnSerializer, GameSerializer, MakeMoveSerializer
import game.api_errors as err


def game_view(request):
    """Главная страница игры"""
    return render(request, "game.html")


@api_view(["POST"])
def end_turn(request):
    """Завершение хода"""
    serializer = EndTurnSerializer(data=request.data)
    if not serializer.is_valid():
        return err.INVALID_DATA.response(status.HTTP_400_BAD_REQUEST)

    game_uid = serializer.validated_data["game_uid"]

    try:
        game = Game.objects.get(uid=game_uid)
    except Game.DoesNotExist:
        return err.GAME_NOT_FOUND.response(status.HTTP_404_NOT_FOUND)

    game.turn_number += 1
    game.save()

    return Response({
        "success": True,
        "turn_number": game.turn_number,
        "active_side": game.active_side,
    })


@api_view(["POST"])
def make_attack(request):
    serializer = MakeMoveSerializer(data=request.data)
    if not serializer.is_valid():
        return err.INVALID_DATA.response(status.HTTP_400_BAD_REQUEST)

    game_uid = serializer.validated_data["game_uid"]
    unit_id = serializer.validated_data["unit_id"]
    to_x = serializer.validated_data["to_x"]
    to_y = serializer.validated_data["to_y"]

    try:
        game = Game.objects.get(uid=game_uid)
        unit = Unit.objects.get(id=unit_id, game=game)
    except Game.DoesNotExist:
        return err.GAME_NOT_FOUND.response(status.HTTP_404_NOT_FOUND)
    except Unit.DoesNotExist:
        return err.UNIT_NOT_FOUND.response(status.HTTP_404_NOT_FOUND)

    if unit.army != game.active_side:
        return err.WRONG_TURN.response(status.HTTP_403_FORBIDDEN)

    dx = to_x - unit.x
    dy = to_y - unit.y

    # Определяем направление и дальность
    is_diag = abs(dx) == abs(dy)
    is_cross = dx == 0 or dy == 0

    if not (is_cross or is_diag):
        return err.INVALID_DIRECTION.response(status.HTTP_400_BAD_REQUEST)

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
        return err.OUT_OF_RANGE.response(status.HTTP_400_BAD_REQUEST)

    # Проверяем путь до цели (не включая цель)
    for step in range(1, distance):
        check_x = unit.x + step_x * step
        check_y = unit.y + step_y * step
        if Unit.objects.filter(game=game, x=check_x, y=check_y).exists():
            return err.PATH_BLOCKED.response(status.HTTP_400_BAD_REQUEST)

    # Проверяем цель
    target_unit = Unit.objects.filter(game=game, x=to_x, y=to_y).first()
    if not target_unit or target_unit.army == unit.army:
        return err.INVALID_TARGET.response(status.HTTP_400_BAD_REQUEST)

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
        unit.save()
        events.append({"type": "move", "unit_id": unit.id, "to_x": to_x, "to_y": to_y})

    return Response({"success": True, "events": events})


@api_view(["POST"])
def make_move(request):
    """Обработка хода"""
    serializer = MakeMoveSerializer(data=request.data)
    if not serializer.is_valid():
        return err.INVALID_DATA.response(status.HTTP_400_BAD_REQUEST)

    game_uid = serializer.validated_data["game_uid"]
    unit_id = serializer.validated_data["unit_id"]
    to_x = serializer.validated_data["to_x"]
    to_y = serializer.validated_data["to_y"]

    try:
        game = Game.objects.get(uid=game_uid)
        unit = Unit.objects.get(id=unit_id, game=game)
    except Game.DoesNotExist:
        return err.GAME_NOT_FOUND.response(status.HTTP_404_NOT_FOUND)
    except Unit.DoesNotExist:
        return err.UNIT_NOT_FOUND.response(status.HTTP_404_NOT_FOUND)

    if unit.army != game.active_side:
        return err.WRONG_TURN.response(status.HTTP_403_FORBIDDEN)

    dx = to_x - unit.x
    dy = to_y - unit.y

    is_diag = abs(dx) == abs(dy)
    is_cross = dx == 0 or dy == 0

    if not (is_cross or is_diag):
        return err.INVALID_DIRECTION.response(status.HTTP_400_BAD_REQUEST)

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
        return err.OUT_OF_RANGE.response(status.HTTP_400_BAD_REQUEST)

    # Проверяем, что путь свободен
    for step in range(1, distance + 1):
        check_x = unit.x + step_x * step
        check_y = unit.y + step_y * step

        if blocker_unit := Unit.objects.filter(game=game, x=check_x, y=check_y).first():
            if blocker_unit.army == unit.army or step < distance:
                return err.PATH_BLOCKED.response(status.HTTP_400_BAD_REQUEST)

    unit.x = to_x
    unit.y = to_y
    unit.save()

    events = [{
        "type": "move",
        "unit_id": unit.id,
        "to_x": to_x,
        "to_y": to_y
    }]
    return Response({"success": True, "events": events})


@api_view(["POST"])
def new_game(request):
    """Создание новой игры"""
    # Временно удаляем игры старше 3 часов
    Game.objects.filter(created_at__lt=timezone.now() - timedelta(hours=3)).delete()

    game = Game.objects.create(
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

    serializer = GameSerializer(game)

    return Response({
        "success": True,
        "game": serializer.data
    })


@api_view(["GET"])
def get_unit_stats(request):
    """Возвращает характеристики всех типов юнитов"""
    return Response(UNIT_STATS)
