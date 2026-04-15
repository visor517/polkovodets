from dataclasses import dataclass
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST


@dataclass
class Error:
    code: str
    message: str

    def response(self, status_code=HTTP_400_BAD_REQUEST):
        return Response({
            "success": False,
            "error": self.message,
            "error_code": self.code,
        }, status=status_code)


# Общие ошибки
INVALID_DATA = Error("INVALID_DATA", "Неверные данные запроса")
SERVER_ERROR = Error("SERVER_ERROR", "Внутренняя ошибка сервера")

# Игра
GAME_NOT_FOUND = Error("GAME_NOT_FOUND", "Игра не найдена")
GAME_FINISHED = Error("GAME_FINISHED", "Игра уже завершена")

# Ходы
WRONG_TURN = Error("WRONG_TURN", "Сейчас не ваш ход")
MOVE_OUT_OF_RANGE = Error("MOVE_OUT_OF_RANGE", "Слишком далеко")
MOVE_INVALID_PATTERN = Error("MOVE_INVALID_PATTERN", "Неправильное направление движения")
CELL_OCCUPIED = Error("CELL_OCCUPIED", "Клетка занята своим юнитом")

# Юниты
UNIT_NOT_FOUND = Error("UNIT_NOT_FOUND", "Юнит не найден")
