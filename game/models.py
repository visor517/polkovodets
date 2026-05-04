import uuid

from django.contrib.auth.models import User
from django.db import models

from game.army import UNIT_TYPE_CHOICES


class Army(models.TextChoices):
    FRENCH = "french", "Франция"
    RUSSIAN = "russian", "Россия"
    AUSTRIAN = "austrian", "Австрия"


class Game(models.Model):
    STATUS_CHOICES = [
        ("waiting", "Ожидание игрока"),
        ("active", "В процессе"),
        ("finished", "Завершена"),
    ]

    uid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="waiting")
    created_at = models.DateTimeField(auto_now_add=True)
    player1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="games_as_player1")
    player2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="games_as_player2", null=True, blank=True)
    turn_number = models.IntegerField(default=1)
    first_side = models.CharField(max_length=10, choices=Army.choices, default=Army.RUSSIAN)
    second_side = models.CharField(max_length=10, choices=Army.choices, default=Army.FRENCH)
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
        
    def get_player_side(self, user) -> str | None:
        if self.player1 == user:
            return self.first_side
        elif self.player2 == user:
            return self.second_side
        return None


class Unit(models.Model):
    game = models.ForeignKey("Game", on_delete=models.CASCADE, related_name="units")
    unit_type = models.CharField(max_length=20, choices=UNIT_TYPE_CHOICES)
    army = models.CharField(max_length=10, choices=Army.choices)
    x = models.IntegerField()
    y = models.IntegerField()
    last_used_turn = models.IntegerField(default=0)
