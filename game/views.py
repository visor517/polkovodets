import json

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .army import Army, UnitType, UNIT_STATS
from .models import Game, Unit


def game_view(request):
    """Главная страница игры"""
    return render(request, "game.html")


@csrf_exempt
@require_http_methods(["POST"])
def new_game(request):
    """Создание новой игры"""
    game = Game.objects.create(
        first_side=Army.RUSSIAN,
        second_side=Army.FRENCH,
    )

    # Начальная расстановка юнитов
    initial_units = [
        {"unit_type": UnitType.INFANTRY, "army": Army.RUSSIAN, "x": 0, "y": 1},
        {"unit_type": UnitType.INFANTRY, "army": Army.RUSSIAN, "x": 0, "y": 2},
        {"unit_type": UnitType.CUIRASSIER, "army": Army.RUSSIAN, "x": 0, "y": 4},
        {"unit_type": UnitType.CUIRASSIER, "army": Army.RUSSIAN, "x": 0, "y": 5},
        {"unit_type": UnitType.HUSSAR, "army": Army.RUSSIAN, "x": 0, "y": 7},
        {"unit_type": UnitType.HUSSAR, "army": Army.RUSSIAN, "x": 0, "y": 8},
        {"unit_type": UnitType.ARTILLERY, "army": Army.RUSSIAN, "x": 2, "y": 5},

        {"unit_type": UnitType.INFANTRY, "army": Army.FRENCH, "x": 8, "y": 3},
        {"unit_type": UnitType.INFANTRY, "army": Army.FRENCH, "x": 8, "y": 4},
        {"unit_type": UnitType.INFANTRY, "army": Army.FRENCH, "x": 8, "y": 5},
        {"unit_type": UnitType.INFANTRY, "army": Army.FRENCH, "x": 8, "y": 6},
        {"unit_type": UnitType.INFANTRY, "army": Army.FRENCH, "x": 9, "y": 3},
        {"unit_type": UnitType.INFANTRY, "army": Army.FRENCH, "x": 9, "y": 4},
        {"unit_type": UnitType.INFANTRY, "army": Army.FRENCH, "x": 9, "y": 5},
        {"unit_type": UnitType.INFANTRY, "army": Army.FRENCH, "x": 9, "y": 6},
    ]

    for unit_data in initial_units:
        Unit.objects.create(game=game, **unit_data)

    # Формируем ответ
    units_dict = {}
    for unit in game.units.all():
        stats = UNIT_STATS[unit.unit_type]
        units_dict[unit.id] = {
            "id": unit.id,
            "type": unit.unit_type,
            "army": unit.army,
            "x": unit.x,
            "y": unit.y,
            "name": stats["name"],
        }

    return JsonResponse({
        "success": True,
        "game_uid": str(game.uid),
        "first_side": game.first_side,
        "second_side": game.second_side,
        "turn_number": game.turn_number,
        "active_side": game.active_side,
        "units": units_dict,
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
            if dx + dy > move_range:
                return JsonResponse({
                    "success": False,
                    "error": "Слишком далеко",
                    "error_code": "MOVE_OUT_OF_RANGE"
                })

        # Проверка, что клетка не занята своим юнитом
        friendly_unit = Unit.objects.filter(game=game, x=to_x, y=to_y, army=unit.army).first()
        if friendly_unit:
            return JsonResponse({
                "success": False,
                "error": "Клетка занята своим юнитом",
                "error_code": "OCCUPIED"
            })

        # Проверка боя с вражеским юнитом
        enemy_unit = Unit.objects.filter(game=game, x=to_x, y=to_y).exclude(army=unit.army).first()

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

            target_unit.delete()
            events.append({
                "type": "destroy",
                "unit_id": target_unit.id
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
