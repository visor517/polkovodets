from rest_framework import serializers

from .models import Game


class EndTurnSerializer(serializers.Serializer):
    game_uid = serializers.UUIDField()


class MakeMoveSerializer(serializers.Serializer):
    game_uid = serializers.UUIDField()
    unit_id = serializers.IntegerField()
    to_x = serializers.IntegerField()
    to_y = serializers.IntegerField()


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
