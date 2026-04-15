from rest_framework import serializers


class EndTurnSerializer(serializers.Serializer):
    game_uid = serializers.UUIDField()
