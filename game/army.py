from django.db import models


class Army(models.TextChoices):
    FRENCH = "french", "Франция"
    RUSSIAN = "russian", "Россия"
    AUSTRIAN = "austrian", "Австрия"


class UnitType(models.TextChoices):
    INFANTRY = "infantry", "Пехота"
    HUSSAR = "hussar", "Гусары"
    CUIRASSIER = "cuirassier", "Кирасиры"
    ARTILLERY = "artillery", "Артиллерия"


UNIT_STATS = {
    UnitType.INFANTRY: {
        "name": "Линейная пехота",
        "move_pattern": "omni",
        "move_range": 1,
        "attack_pattern": "diagonal",
        "attack_range": 1,
        "charges": True,
        "icon": "⚔",
        "cost": 1,
        "cross_country": False,
    },
    UnitType.HUSSAR: {
        "name": "Гусары",
        "move_pattern": "diagonal",
        "move_range": 3,
        "attack_pattern": "diagonal",
        "attack_range": 3,
        "charges": True,
        "icon": "🐎",
        "cost": 2,
        "cross_country": False,
    },
    UnitType.CUIRASSIER: {
        "name": "Кирасиры",
        "move_pattern": "cross",
        "move_range": 4,
        "attack_pattern": "cross",
        "attack_range": 4,
        "charges": True,
        "icon": "🏇",
        "cost": 4,
        "cross_country": False,
    },
    UnitType.ARTILLERY: {
        "name": "Артиллерия",
        "move_pattern": "omni",
        "move_range": 1,
        "attack_pattern": "omni",
        "attack_range": 5,
        "charges": False,
        "icon": "💣",
        "cost": 10,
        "cross_country": False,
    },
}
