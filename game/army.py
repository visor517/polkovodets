from django.db import models


class Army(models.TextChoices):
    FRENCH = "french", "Франция"
    RUSSIAN = "russian", "Россия"
    AUSTRIAN = "austrian", "Австрия"


UNIT_STATS = {
    "infantry": {
        "name": "Линейная пехота",
        "move": {"cross": 1, "diag": 1},
        "attack": {"cross": 0, "diag": 1},
        "charges": True,
        "icon": "⚔️",
        "cost": 1,
        "cross_country": False,
        "images": {
            "french": "/static/images/fr_infantry.png",
            "russian": "/static/images/rus_infantry.png",
        }
    },
    "hussar": {
        "name": "Гусары",
        "move": {"cross": 0, "diag": 3},
        "attack": {"cross": 0, "diag": 3},
        "charges": True,
        "icon": "🐎",
        "cost": 2,
        "cross_country": False,
        "images": {
            "french": "/static/images/fr_hussar.png",
            "russian": "/static/images/rus_hussar.png",
        }
    },
    "dragoon": {
        "name": "Драгуны",
        "move": {"cross": 1, "diag": 2},
        "attack": {"cross": 1, "diag": 2},
        "charges": True,
        "icon": "🐎",
        "cost": 3,
        "cross_country": False,
        "images": {
            "french": "/static/images/fr_dragoon.png",
            "russian": "/static/images/rus_dragoon.png",
        }
    },
    "cuirassier": {
        "name": "Кирасиры",
        "move": {"cross": 4, "diag": 0},
        "attack": {"cross": 4, "diag": 0},
        "charges": True,
        "icon": "🏇",
        "cost": 4,
        "cross_country": False,
        "images": {
            "french": "/static/images/fr_cuirassier.png",
            "russian": "/static/images/rus_cuirassier.png",
        }
    },
    "artillery": {
        "name": "Артиллерия",
        "move": {"cross": 1, "diag": 1},
        "attack": {"cross": 5, "diag": 5},
        "charges": False,
        "icon": "💣",
        "cost": 10,
        "cross_country": False,
        "images": {
            "french": "/static/images/fr_artillery.png",
            "russian": "/static/images/rus_artillery.png",
        }
    },
    "horse_artillery": {
        "name": "Конная артиллерия",
        "move": {"cross": 1, "diag": 2},
        "attack": {"cross": 5, "diag": 5},
        "charges": False,
        "icon": "💣",
        "cost": 15,
        "cross_country": False,
        "images": {
            "french": "/static/images/fr_horse_artillery.png",
            "russian": "/static/images/rus_horse_artillery.png",
        }
    },
}

UNIT_TYPE_CHOICES = [(key, data["name"]) for key, data in UNIT_STATS.items()]
