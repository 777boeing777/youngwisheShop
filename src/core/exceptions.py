from fastapi.exceptions import HTTPException


class UniqueConstraintError(HTTPException):
    """Ограничение на уникальность объектов"""


class NotFoundErrorError(HTTPException):
    """Страница/объект не найден-а"""
