from django.contrib import admin
from .models import Game, Unit


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ("uid", "created_at", "turn_number", "first_side", "second_side", "is_finished")
    list_filter = ("first_side", "is_finished", "created_at")
    search_fields = ("uid",)
    readonly_fields = ("uid", "created_at")
    ordering = ("-created_at",)


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ("id", "game", "unit_type", "army", "x", "y")
    list_filter = ("unit_type", "army", "game")
    search_fields = ("game__uid",)
    ordering = ("game", "id")
