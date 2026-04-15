import uuid
from django.db import models

from .army import Army, UnitType


class Game(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    turn_number = models.IntegerField(default=1)
    first_side = models.CharField(max_length=10, choices=Army.choices, default=Army.RUSSIAN)
    second_side = models.CharField(max_length=10, choices=Army.choices, default=Army.FRENCH)
    is_finished = models.BooleanField(default=False)
    winner = models.CharField(max_length=10, choices=Army.choices, blank=True, null=True)

    @property
    def active_side(self):
        """Кто ходит сейчас"""
        return self.first_side if self.turn_number % 2 == 1 else self.second_side

    def check_winner(self) -> str | None:
        first_side_units = self.units.filter(army=self.first_side).count()
        second_side_units = self.units.filter(army=self.second_side).count()

        if first_side_units == 0:
            self.winner = self.second_side
            self.is_finished = True
            self.save()
            return self.second_side
        if second_side_units == 0:
            self.winner = self.first_side
            self.is_finished = True
            self.save()
            return self.first_side


class Unit(models.Model):
    game = models.ForeignKey("Game", on_delete=models.CASCADE, related_name="units")
    unit_type = models.CharField(max_length=20, choices=UnitType.choices)
    army = models.CharField(max_length=10, choices=Army.choices)
    x = models.IntegerField()
    y = models.IntegerField()
