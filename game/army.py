from django.db import models


class Army(models.TextChoices):
    FRENCH = "french", "Франция"
    RUSSIAN = "russian", "Россия"
    AUSTRIAN = "austrian", "Австрия"


UNIT_STATS = {
    "infantry": {
        "name": "Линейная пехота",
        "move_pattern": "omni",
        "move_range": 1,
        "attack_pattern": "diagonal",
        "attack_range": 1,
        "charges": True,
        "icon": "⚔️",
        "cost": 1,
        "cross_country": False,
        "images": {
            "french": "/static/images/fr_infantry.png",
            "russian": "/static/images/rus_infantry.png"
        }
    },
    "hussar": {
        "name": "Гусары",
        "move_pattern": "diagonal",
        "move_range": 3,
        "attack_pattern": "diagonal",
        "attack_range": 3,
        "charges": True,
        "icon": "🐎",
        "cost": 2,
        "cross_country": False,
        "images": {
            "french": "/static/images/fr_hussar.png",
            "russian": "/static/images/rus_hussar.png"
        }
    },
    "cuirassier": {
        "name": "Кирасиры",
        "move_pattern": "cross",
        "move_range": 4,
        "attack_pattern": "cross",
        "attack_range": 4,
        "charges": True,
        "icon": "🏇",
        "cost": 4,
        "cross_country": False,
        "images": {
            "french": "/static/images/fr_cuirassier.png",
            "russian": "/static/images/rus_cuirassier.png"
        }
    },
    "artillery": {
        "name": "Артиллерия",
        "move_pattern": "omni",
        "move_range": 1,
        "attack_pattern": "omni",
        "attack_range": 5,
        "charges": False,
        "icon": "💣",
        "cost": 10,
        "cross_country": False,
        "images": {
            "french": "/static/images/fr_artillery.png",
            "russian": "/static/images/rus_artillery.png"
        }
    }
}

UNIT_TYPE_CHOICES = [(key, data["name"]) for key, data in UNIT_STATS.items()]
