from __future__ import annotations
from typing import TYPE_CHECKING
from src.core.sql.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (
    ForeignKey,
    String,
    Integer,
    DateTime,
    Float,
    Boolean,
    func,
    SmallInteger,
)
from datetime import datetime
from src.core.mixins import JSONRepresentationMixin
from sqlalchemy.dialects.postgresql import JSONB

if TYPE_CHECKING:
    from src.core.users.models import User


class Company(JSONRepresentationMixin, Base):
    __tablename__ = "companies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(
        "Название компании",
        String(length=256),
        unique=True,
        index=True,
    )
    director_fullname: Mapped[str] = mapped_column("ФИО директора", String(length=64))
    type: Mapped[int] = mapped_column("Тип компании", SmallInteger)
    jur_address: Mapped[JSONB] = mapped_column(
        "Юридический адрес",
        JSONB,
        nullable=True,
    )
    fact_address: Mapped[JSONB] = mapped_column(
        "Фактический адрес",
        JSONB,
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        "Дата регистрации",
        DateTime(timezone=True),
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        "Дата обновления",
        DateTime(timezone=True),
        nullable=True,
    )
    rating: Mapped[float] = mapped_column("Рейтинг", Float, nullable=True, index=True)
    is_hidden: Mapped[bool] = mapped_column("Скрыта в системе", Boolean, default=False)
    is_verified: Mapped[bool] = mapped_column("Подтверждена", Boolean, default=False)
    employees: Mapped[list[Employee]] = relationship("Employee", backref="company")

    def __repr__(self):
        return self.name


class Employee(JSONRepresentationMixin, Base):
    __tablename__ = "employees"

    company_id: Mapped[int] = mapped_column(
        ForeignKey("companies.id"),
        primary_key=True,
        index=True,
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        index=True,
        primary_key=True,
    )
    telegram: Mapped[str] = mapped_column(
        "Ссылка на телеграм",
        String(length=256),
        nullable=True,
    )
    vk: Mapped[str] = mapped_column("Ссылка на ВК", String(length=256), nullable=True)
    phone_number: Mapped[str] = mapped_column(
        "Номер телефона",
        String(length=32),
        nullable=True,
    )
    extra_data: Mapped[str] = mapped_column(
        "Дополнительная информация о сотруднике",
        String,
        nullable=True,
    )
    user: Mapped[User] = relationship(
        "User",
        backref="employee",
        lazy="joined",
        uselist=False,
    )

    def __repr__(self) -> str:
        return f"Employee(user={self.user}, company={self.company})"
