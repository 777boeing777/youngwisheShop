from pydantic import BaseModel


class BaseErrorModel(BaseModel):
    detail: str


class UniqueConstraint(BaseErrorModel):
    class Config:
        json_schema_extra = {
            "example": {
                "detail": "Компания с названием $COMPANY_NAME уже существует в системе",
            },
        }


class Unauthorized(BaseErrorModel):
    class Config:
        json_schema_extra = {"example": {"detail": "Не авторизован"}}


class NotFound(BaseErrorModel):
    class Config:
        json_schema_extra = {"example": {"detail": "Объект не существует"}}
