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
UNIT_NOT_FOUND = Error("UNIT_NOT_FOUND", "Юнит не найден")

# Ходы
CELL_OCCUPIED = Error("CELL_OCCUPIED", "Клетка занята своим юнитом")
INVALID_PATTERN = Error("INVALID_PATTERN", "Неправильное направление")
INVALID_TARGET = Error("INVALID_TARGET", "Некорректная цель")
OUT_OF_RANGE = Error("OUT_OF_RANGE", "Слишком далеко")
WRONG_TURN = Error("WRONG_TURN", "Сейчас не ваш ход")
