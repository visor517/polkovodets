from django.contrib import admin

from game.models import Game, Unit

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ("uid", "status", "created_at", "turn_number", "first_side", "second_side", "winner")
    list_filter = ("status", "first_side", "second_side", "winner", "created_at")
    search_fields = ("uid",)
    readonly_fields = ("uid", "created_at")
    ordering = ("-created_at",)
    
    fieldsets = (
        (None, {
            "fields": ("uid", "status", "created_at")
        }),
        ("Игроки", {
            "fields": ("player1", "player2")
        }),
        ("Игровая информация", {
            "fields": ("turn_number", "first_side", "second_side", "winner")
        }),
    )


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ("id", "game", "unit_type", "army", "x", "y", "last_used_turn")
    list_filter = ("unit_type", "army", "game")
    search_fields = ("game__uid",)
    ordering = ("game", "id")
