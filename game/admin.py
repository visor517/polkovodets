from django.contrib import admin

from game.models import Game, Unit

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "uid", "status", "player1", "player1_side", "player2", "player2_side",
                    "round_number", "active_side")
    list_filter = ("status", "player1_side", "player2_side", "winner", "created_at")
    search_fields = ("uid", "name")
    readonly_fields = ("uid", "created_at", "round_number", "active_side")
    ordering = ("-id",)

    fieldsets = (
        (None, {
            "fields": ("uid", "name", "status", "created_at")
        }),
        ("Игроки", {
            "fields": ("player1", "player1_side", "player1_mr", "player1_score",
                       "player2", "player2_side", "player2_mr", "player2_score")
        }),
        ("Игровое состояние", {
            "fields": ("move_number", "round_number", "active_side", "winner", "is_finished")
        }),
    )


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ("id", "game", "unit_type", "army", "x", "y", "last_used_turn")
    list_filter = ("unit_type", "army", "game")
    search_fields = ("game__uid",)
    ordering = ("game", "id")
