from rest_framework import serializers

from . import exceptions as err
from .models import Game, Unit


class EndTurnSerializer(serializers.Serializer):
    game_uid = serializers.UUIDField()

    def validate(self, data):
        try:
            game = Game.objects.get(uid=data["game_uid"])
        except Game.DoesNotExist:
            raise serializers.ValidationError("Игра не найдена")

        data["game"] = game
        return data


class UnitActionSerializer(serializers.Serializer):
    game_uid = serializers.UUIDField()
    unit_id = serializers.IntegerField()
    to_x = serializers.IntegerField()
    to_y = serializers.IntegerField()

    def validate(self, data):
        try:
            game = Game.objects.get(uid=data["game_uid"])
        except Game.DoesNotExist:
            raise err.GameNotFound()

        try:
            unit = Unit.objects.get(id=data["unit_id"], game=game)
        except Unit.DoesNotExist:
            raise err.UnitNotFound()

        if unit.army != game.active_side:
            raise err.WrongTurn()

        data["game"] = game
        data["unit"] = unit
        return data


class GameSerializer(serializers.ModelSerializer):
    active_side = serializers.ReadOnlyField()
    units = serializers.SerializerMethodField()

    class Meta:
        model = Game
        fields = ["uid", "first_side", "second_side", "turn_number", "active_side", "is_finished", "units"]

    def get_units(self, obj):
        from .army import UNIT_STATS
        units_dict = {}
        for unit in obj.units.all():
            stats = UNIT_STATS[unit.unit_type]
            units_dict[unit.id] = {
                "id": unit.id,
                "type": unit.unit_type,
                "army": unit.army,
                "x": unit.x,
                "y": unit.y,
                "name": stats["name"],
            }
        return units_dict
