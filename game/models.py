import uuid

from django.contrib.auth.models import User
from django.db import models

from game.army import UNIT_TYPE_CHOICES


class Army(models.TextChoices):
    FRENCH = "french", "Французская армия"
    RUSSIAN = "russian", "Русская армия"
    # AUSTRIAN = "austrian", "Австрия армия"


class Game(models.Model):
    STATUS_CHOICES = [
        ("waiting", "Ожидание игрока"),
        ("active", "В процессе"),
        ("finished", "Завершена"),
    ]

    id = models.AutoField(primary_key=True)
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="waiting")
    created_at = models.DateTimeField(auto_now_add=True)
    world_width = models.IntegerField(default=16)
    world_height = models.IntegerField(default=12)
    player1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="games_as_player1")
    player2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="games_as_player2", null=True, blank=True)
    player1_side = models.CharField(max_length=10, choices=Army.choices)
    player2_side = models.CharField(max_length=10, choices=Army.choices)
    player1_mr = models.IntegerField(default=100)
    player2_mr = models.IntegerField(default=100)
    player1_score = models.IntegerField(default=0)
    player2_score = models.IntegerField(default=0)
    is_player1_first = models.BooleanField(default=True)
    move_number = models.IntegerField(default=1)
    winner = models.CharField(max_length=10, choices=Army.choices, blank=True, null=True)
    is_finished = models.BooleanField(default=False)

    @property
    def round_number(self):
        """Номер тура (оба игрока сделали ход = 1 тур)"""
        return (self.move_number + 1) // 2

    @property
    def active_side(self):
        """Какая сторона ходит сейчас"""
        sides = (self.player1_side, self.player2_side) \
            if self.is_player1_first else (self.player2_side, self.player1_side)
        return sides[self.move_number % 2 == 0]

    def check_winner(self):
        """Проверка победителя"""
        player1_units = self.units.filter(army=self.player1_side).count()
        player2_units = self.units.filter(army=self.player2_side).count()

        if player1_units == 0:
            self.winner = self.player2_side
            self.is_finished = True
            self.save()
            return self.player2_side
        if player2_units == 0:
            self.winner = self.player1_side
            self.is_finished = True
            self.save()
            return self.player1_side
        return None

    def get_active_side_display(self):
        return Army(self.active_side).label


class Unit(models.Model):
    game = models.ForeignKey("Game", on_delete=models.CASCADE, related_name="units")
    unit_type = models.CharField(max_length=20, choices=UNIT_TYPE_CHOICES)
    army = models.CharField(max_length=10, choices=Army.choices)
    x = models.IntegerField()
    y = models.IntegerField()
    last_used_turn = models.IntegerField(default=0)
