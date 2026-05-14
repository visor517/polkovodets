from django.urls import path
from . import views


urlpatterns = [
    path("", views.lobby_view, name="lobby"),
    path("game/create/", views.create_game_view, name="create_game"),
    path("game/<str:game_uid>/", views.game_view, name="game"),
    path("game/<str:game_uid>/join/", views.join_game_view, name="join_game"),
    path("rules/", views.rules_view, name="rules"),
    path("api/attack/", views.make_attack, name="make_attack"),
    path("api/end_turn/", views.end_turn, name="end_turn"),
    path("api/move/", views.make_move, name="make_move"),
]
