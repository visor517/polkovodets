from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status

from .models import Army, Game, Unit


class GameAPITestCase(APITestCase):

    def setUp(self):
        # Создаём тестовую игру
        self.game = Game.objects.create(
            first_side=Army.RUSSIAN,
            second_side=Army.FRENCH
        )

        # Создаём тестового юнита
        self.unit = Unit.objects.create(
            game=self.game,
            unit_type="infantry",
            army=Army.RUSSIAN,
            x=5,
            y=5
        )

    def test_new_game_success(self):
        url = reverse("new_game")
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["success"])
        self.assertIn("game", response.data)

        game_data = response.data["game"]
        self.assertIn("uid", game_data)
        self.assertIn("units", game_data)
        self.assertIn("first_side", game_data)
        self.assertIn("second_side", game_data)
        self.assertIn("active_side", game_data)
        self.assertIn("turn_number", game_data)
