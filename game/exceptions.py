from rest_framework.exceptions import APIException
from rest_framework import status


class GameNotFound(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "Игра не найдена"
    default_code = "game_not_found"


class UnitNotFound(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "Юнит не найден"
    default_code = "unit_not_found"


class UnitAlreadyActed(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Этот юнит уже действовал в этом ходу"
    default_code = "unit_already_acted"


class WrongTurn(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = "Сейчас не ваш ход"
    default_code = "wrong_turn"


class OutOfRange(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Слишком далеко"
    default_code = "out_of_range"


class PathBlocked(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Путь заблокирован"
    default_code = "path_blocked"


class InvalidDirection(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Недопустимое направление"
    default_code = "invalid_direction"


class InvalidTarget(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Некорректная цель"
    default_code = "invalid_target"
