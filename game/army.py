UNIT_STATS = {
    "infantry": {
        "name": "Линейная пехота",
        "move": {"cross": 1, "diag": 1},
        "attack": {"cross": 0, "diag": 1},
        "charges": True,
        "icon": "⚔️",
        "cost": 1,
        "terrain": {
            "forest": {"enter": True, "fight": False},
            "mountain": {"enter": True, "fight": False},
        },
        "images": {
            "french": "/static/images/fr_infantry.png",
            "russian": "/static/images/rus_infantry.png",
        }
    },
    "grenadier": {
        "name": "Гренадёры",
        "move": {"cross": 1, "diag": 1},
        "attack": {"cross": 1, "diag": 1},
        "charges": True,
        "icon": "Гр️",
        "cost": 2,
        "terrain": {
            "forest": {"enter": True, "fight": False},
            "mountain": {"enter": True, "fight": False},
        },
        "images": {
            "french": "/static/images/fr_grenadier.png",
            "russian": "/static/images/rus_grenadier.png",
        }
    },
    "huntsman": {
        "name": "Егеря",
        "move": {"cross": 1, "diag": 1},
        "attack": {"cross": 0, "diag": 1},
        "charges": True,
        "icon": "Ег️",
        "cost": 2,
        "terrain": {
            "forest": {"enter": True, "fight": True},
            "mountain": {"enter": True, "fight": True},
        },
        "images": {
            "french": "/static/images/fr_huntsman.png",
            "russian": "/static/images/rus_huntsman.png",
        }
    },
    "guardsman": {
        "name": "Гвардейская пехота",
        "move": {"cross": 1, "diag": 1},
        "attack": {"cross": 1, "diag": 1},
        "charges": True,
        "icon": "Гв️",
        "cost": 2.5,
        "terrain": {
            "forest": {"enter": True, "fight": True},
            "mountain": {"enter": True, "fight": True},
        },
        "images": {
            "french": "/static/images/fr_guardsman.png",
            "russian": "/static/images/rus_guardsman.png",
        }
    },
    "dragoon": {
        "name": "Драгуны",
        "move": {"cross": 1, "diag": 2},
        "attack": {"cross": 1, "diag": 2},
        "charges": True,
        "icon": "🐎",
        "cost": 3,
        "terrain": {
            "forest": {"enter": True, "fight": False},
            "mountain": {"enter": False, "fight": False},
        },
        "images": {
            "french": "/static/images/fr_dragoon.png",
            "russian": "/static/images/rus_dragoon.png",
        }
    },
    "hussar": {
        "name": "Гусары",
        "move": {"cross": 0, "diag": 3},
        "attack": {"cross": 0, "diag": 3},
        "charges": True,
        "icon": "🐎",
        "cost": 3,
        "terrain": {
            "forest": {"enter": True, "fight": False},
            "mountain": {"enter": False, "fight": False},
        },
        "images": {
            "french": "/static/images/fr_hussar.png",
            "russian": "/static/images/rus_hussar.png",
        }
    },
    "ulan": {
        "name": "Уланы",
        "move": {"cross": 0, "diag": 3},
        "attack": {"cross": 0, "diag": 3},
        "charges": True,
        "icon": "Ул",
        "cost": 3,
        "terrain": {
            "forest": {"enter": True, "fight": False},
            "mountain": {"enter": False, "fight": False},
        },
        "images": {
            "french": "/static/images/fr_ulan.png",
            "russian": "/static/images/rus_ulan.png",
        }
    },
    "horse_huntsman": {
        "name": "Конные егеря",
        "move": {"cross": 0, "diag": 3},
        "attack": {"cross": 0, "diag": 3},
        "charges": True,
        "icon": "Ке",
        "cost": 3.5,
        "terrain": {
            "forest": {"enter": True, "fight": True},
            "mountain": {"enter": True, "fight": True},
        },
        "images": {
            "french": "/static/images/fr_horse_huntsman.png",
            "russian": "/static/images/rus_horse_huntsman.png",
        }
    },
    "cuirassier": {
        "name": "Кирасиры",
        "move": {"cross": 4, "diag": 0},
        "attack": {"cross": 4, "diag": 0},
        "charges": True,
        "icon": "🏇",
        "cost": 4,
        "terrain": {
            "forest": {"enter": True, "fight": False},
            "mountain": {"enter": False, "fight": False},
        },
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
        "terrain": {
            "forest": {"enter": True, "fight": False},
            "mountain": {"enter": False, "fight": False},
        },
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
        "terrain": {
            "forest": {"enter": True, "fight": False},
            "mountain": {"enter": False, "fight": False},
        },
        "images": {
            "french": "/static/images/fr_horse_artillery.png",
            "russian": "/static/images/rus_horse_artillery.png",
        }
    },
}

UNIT_TYPE_CHOICES = [(key, data["name"]) for key, data in UNIT_STATS.items()]
