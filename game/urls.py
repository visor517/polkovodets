from django.urls import path
from . import views


urlpatterns = [
    path("", views.game_view, name="game"),
    path("api/move/", views.make_move, name="make_move"),
]
