from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json


def game_view(request):
    """Главная страница игры"""
    return render(request, "game.html")


@csrf_exempt
@require_http_methods(["POST"])
def make_move(request):
    """Обработка хода"""
    try:
        data = json.loads(request.body)

        unit_id = data.get("unit_id")
        to_x = data.get("to_x")
        to_y = data.get("to_y")

        # Имитация - просто возвращаем то, что прислали
        return JsonResponse({
            "success": True,
            "events": [
                {
                    "type": "move",
                    "unit_id": unit_id,
                    "to_x": to_x,
                    "to_y": to_y
                }
            ]
        })
        
    except Exception as e:
        return JsonResponse({
            "success": False,
            "error": str(e)
        })
