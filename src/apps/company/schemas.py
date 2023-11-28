from __future__ import annotations
from pydantic import BaseModel, Field
from src.apps.company.enums import CompanyType
from datetime import datetime


class BaseCompany(BaseModel):
    name: str = Field(
        ...,
        max_length=256,
        min_length=2,
        title="Название компании",
        unique=True,
    )
    director_fullname: str = Field(..., max_length=64, title="Полное имя директора")
    type: CompanyType = Field(
        ...,
        title="Тип компании",
        description="1 - Индивидуальный предприниматель, 2 - Юридическое лица",
    )
    jur_address: dict = Field(..., title="Юридический адрес")
    fact_address: dict = Field(..., title="Фактический адрес")


class CompanyIn(BaseCompany):
    ...


class CompanyOut(BaseCompany):
    id: int
    created_at: datetime = Field(..., title="Дата регистрации")
    updated_at: datetime = Field(..., title="Дата последнего обновления")
    rating: float | None = Field(..., title="Рейтинг")

    class ConfigDict:
        from_attributes = True
