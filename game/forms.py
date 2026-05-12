from django import forms
from django.contrib.auth.models import User

from game.models import Army


class CreateGameForm(forms.Form):
    name = forms.CharField(max_length=100, label="Название игры")
    game_type = forms.ChoiceField(
        choices=[("local", "На одном компьютере"), ("online", "На разных компьютерах")],
        label="Тип игры",
        initial="online"
    )

    # Первый игрок (создатель)
    player1_mr = forms.IntegerField(min_value=50, max_value=200, initial=100, label="МР первого игрока")
    player1_side = forms.ChoiceField(choices=Army.choices, label="Сторона первого игрока")

    # Второй игрок
    player2_mr = forms.IntegerField(min_value=50, max_value=200, initial=100, label="МР второго игрока")
    player2_side = forms.ChoiceField(choices=Army.choices, label="Сторона второго игрока")
    player2_identifier = forms.CharField(
        max_length=150,
        required=False,
        label="Второй игрок (логин или email)",
        help_text="Если оставить пустым, игра будет ожидать игрока"
    )

    first_turn = forms.ChoiceField(
        choices=[("player1", "Первый игрок"), ("player2", "Второй игрок")],
        label="Кто ходит первым",
        initial="player1"
    )

    def clean(self):
        cleaned_data = super().clean()

        if cleaned_data.get("player1_side") == cleaned_data.get("player2_side"):
            self.add_error("player2_side", "Эта сторона уже выбрана первым игроком")

        # Определяем второго игрока
        game_type = cleaned_data.get("game_type")
        player2_identifier = cleaned_data.get("player2_identifier")

        if game_type == "online" and player2_identifier:
            try:
                if "@" in player2_identifier:
                    player2 = User.objects.get(email=player2_identifier)
                else:
                    player2 = User.objects.get(username=player2_identifier)
                cleaned_data["player2"] = player2
                cleaned_data["status"] = "active"
            except User.DoesNotExist:
                self.add_error("player2_identifier", "Пользователь не найден")
        elif game_type == "local":
            cleaned_data["status"] = "active"
        else:
            cleaned_data["status"] = "waiting"

        return cleaned_data
