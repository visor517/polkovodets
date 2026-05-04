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

        if unit.last_used_turn == game.turn_number:
            raise err.UnitAlreadyActed()

        data["game"] = game
        data["unit"] = unit
        return data


class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = "__all__"


class GameSerializer(serializers.ModelSerializer):
    active_side = serializers.ReadOnlyField()
    units = serializers.SerializerMethodField()
    status = serializers.CharField(source="get_status_display")
    winner_display = serializers.CharField(source="get_winner_display", read_only=True)

    class Meta:
        model = Game
        fields = [
            "uid", "status", "created_at",
            "player1", "player2",
            "turn_number", "first_side", "second_side",
            "active_side", "winner", "winner_display",
            "units"
        ]

    def get_units(self, obj):
        units_dict = {}
        for unit in obj.units.all():
            units_dict[unit.id] = {
                "id": unit.id,
                "unit_type": unit.unit_type,
                "army": unit.army,
                "x": unit.x,
                "y": unit.y,
                "last_used_turn": unit.last_used_turn,
            }
        return units_dict
