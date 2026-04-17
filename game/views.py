from datetime import timedelta
import json

from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .army import Army, UnitType, UNIT_STATS
from .models import Game, Unit
from .serializers import EndTurnSerializer, GameSerializer
import game.api_errors as err


def game_view(request):
    """Главная страница игры"""
    return render(request, "game.html")


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
        {"unit_type": UnitType.INFANTRY, "army": Army.RUSSIAN, "x": 1, "y": 4},
        {"unit_type": UnitType.INFANTRY, "army": Army.RUSSIAN, "x": 1, "y": 5},
        {"unit_type": UnitType.INFANTRY, "army": Army.RUSSIAN, "x": 1, "y": 6},
        {"unit_type": UnitType.INFANTRY, "army": Army.RUSSIAN, "x": 1, "y": 7},
        {"unit_type": UnitType.INFANTRY, "army": Army.RUSSIAN, "x": 2, "y": 4},
        {"unit_type": UnitType.INFANTRY, "army": Army.RUSSIAN, "x": 2, "y": 5},
        {"unit_type": UnitType.INFANTRY, "army": Army.RUSSIAN, "x": 2, "y": 6},
        {"unit_type": UnitType.INFANTRY, "army": Army.RUSSIAN, "x": 2, "y": 7},
        {"unit_type": UnitType.ARTILLERY, "army": Army.RUSSIAN, "x": 3, "y": 5},
        {"unit_type": UnitType.ARTILLERY, "army": Army.RUSSIAN, "x": 3, "y": 6},
        {"unit_type": UnitType.CUIRASSIER, "army": Army.RUSSIAN, "x": 2, "y": 1},
        {"unit_type": UnitType.CUIRASSIER, "army": Army.RUSSIAN, "x": 2, "y": 2},
        {"unit_type": UnitType.HUSSAR, "army": Army.RUSSIAN, "x": 2, "y": 9},
        {"unit_type": UnitType.HUSSAR, "army": Army.RUSSIAN, "x": 2, "y": 10},

        {"unit_type": UnitType.INFANTRY, "army": Army.FRENCH, "x": 10, "y": 4},
        {"unit_type": UnitType.INFANTRY, "army": Army.FRENCH, "x": 10, "y": 5},
        {"unit_type": UnitType.INFANTRY, "army": Army.FRENCH, "x": 10, "y": 6},
        {"unit_type": UnitType.INFANTRY, "army": Army.FRENCH, "x": 10, "y": 7},
        {"unit_type": UnitType.INFANTRY, "army": Army.FRENCH, "x": 9, "y": 4},
        {"unit_type": UnitType.INFANTRY, "army": Army.FRENCH, "x": 9, "y": 5},
        {"unit_type": UnitType.INFANTRY, "army": Army.FRENCH, "x": 9, "y": 6},
        {"unit_type": UnitType.INFANTRY, "army": Army.FRENCH, "x": 9, "y": 7},
        {"unit_type": UnitType.ARTILLERY, "army": Army.FRENCH, "x": 8, "y": 5},
        {"unit_type": UnitType.ARTILLERY, "army": Army.FRENCH, "x": 8, "y": 6},
        {"unit_type": UnitType.CUIRASSIER, "army": Army.FRENCH, "x": 9, "y": 1},
        {"unit_type": UnitType.CUIRASSIER, "army": Army.FRENCH, "x": 9, "y": 2},
        {"unit_type": UnitType.HUSSAR, "army": Army.FRENCH, "x": 9, "y": 9},
        {"unit_type": UnitType.HUSSAR, "army": Army.FRENCH, "x": 9, "y": 10},
    ]

    for unit_data in initial_units:
        Unit.objects.create(game=game, **unit_data)

    serializer = GameSerializer(game)

    return Response({
        "success": True,
        "game": serializer.data
    })


@csrf_exempt
@require_http_methods(["POST"])
def make_move(request):
    """Обработка хода"""
    try:
        data = json.loads(request.body)

        game_uid = data.get("game_uid")
        unit_id = data.get("unit_id")
        to_x = data.get("to_x")
        to_y = data.get("to_y")

        game = Game.objects.get(uid=game_uid)
        unit = Unit.objects.get(id=unit_id, game=game)

        if unit.army != game.active_side:
            return JsonResponse({
                "success": False,
                "error": "Сейчас не ваш ход",
                "error_code": "WRONG_TURN"
            })

        move_range = UNIT_STATS[unit.unit_type]["move_range"]
        move_pattern = UNIT_STATS[unit.unit_type]["move_pattern"]

        dx = abs(to_x - unit.x)
        dy = abs(to_y - unit.y)

        if move_pattern == "cross":
            if dx + dy > move_range or (dx != 0 and dy != 0):
                return JsonResponse({
                    "success": False,
                    "error": "Слишком далеко или не по правилам",
                    "error_code": "MOVE_OUT_OF_RANGE"
                })
        elif move_pattern == "diagonal":
            if dx != dy or dx > move_range:
                return JsonResponse({
                    "success": False,
                    "error": "Слишком далеко или не по правилам",
                    "error_code": "MOVE_OUT_OF_RANGE"
                })
        else:  # omni
            if max(dx, dy) > move_range:
                return JsonResponse({
                    "success": False,
                    "error": "Слишком далеко",
                    "error_code": "MOVE_OUT_OF_RANGE"
                })

        events = []

        # Проверяем, есть ли кто-то на целевой клетке
        target_unit = Unit.objects.filter(game=game, x=to_x, y=to_y).first()

        if target_unit:
            # Если это свой юнит — ошибка
            if target_unit.army == unit.army:
                return JsonResponse({
                    "success": False,
                    "error": "Клетка занята своим юнитом",
                    "error_code": "OCCUPIED"
                })
            events.append({
                "type": "destroy",
                "unit_id": target_unit.id
            })
            target_unit.delete()

            # проверка на конец игры
            if winner := game.check_winner():
                events.append({
                    "type": "game_over",
                    "winner": winner
                })

        # Перемещаем юнита
        unit.x = to_x
        unit.y = to_y
        unit.save()

        events.append({
            "type": "move",
            "unit_id": unit.id,
            "to_x": to_x,
            "to_y": to_y
        })

        return JsonResponse({
            "success": True,
            "events": events
        })
        
    except Exception as e:
        return JsonResponse({
            "success": False,
            "error": str(e)
        })


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
