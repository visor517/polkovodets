from django.urls import path
from . import views


urlpatterns = [
    path("", views.game_view, name="game"),
    path("api/attack/", views.make_attack, name="make_attack"),
    path("api/end_turn/", views.end_turn, name="end_turn"),
    path("api/move/", views.make_move, name="make_move"),
    path("api/new_game/", views.new_game, name="new_game"),
]
