from __future__ import annotations
from datetime import datetime

from sqlalchemy import String, Integer, DateTime, Boolean, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from fastapi_users.db import SQLAlchemyBaseUserTable

from src.core.sql.database import Base
from src.core.mixins import JSONRepresentationMixin
from src.apps.company.models import Employee


class User(JSONRepresentationMixin, SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )
    first_name: Mapped[str] = mapped_column(String(length=64), nullable=True)
    last_name: Mapped[str] = mapped_column(String(length=64), nullable=True)
    middle_name: Mapped[str] = mapped_column(String(length=64), nullable=True)
    email: Mapped[str] = mapped_column(
        String(length=320),
        unique=True,
        index=True,
        nullable=False,
    )
    hashed_password: Mapped[str] = mapped_column(String(length=1024), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    joined_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    last_login: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    roles: Mapped[list[Role]] = relationship(
        "UserRoleAssociation",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="joined",
    )
    employee: Mapped[Employee] = relationship(
        "Employee",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="joined",
    )

    def __repr__(self) -> str:
        return self.email


class Role(JSONRepresentationMixin, Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(length=64), nullable=False)
    users: Mapped[list[User]] = relationship(
        "UserRoleAssociation",
        back_populates="role",
        cascade="all, delete-orphan",
        lazy="joined",
    )

    def __repr__(self) -> str:
        return self.name


class UserRoleAssociation(JSONRepresentationMixin, Base):
    __tablename__ = "users_roles"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("roles.id"),
        primary_key=True,
        index=True,
    )
    role_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        primary_key=True,
        index=True,
    )
    expire_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    user: Mapped[User] = relationship(
        "User",
        back_populates="roles",
        lazy="joined",
    )
    role: Mapped[Role] = relationship(
        "Role",
        back_populates="users",
        lazy="joined",
    )

    def __repr__(self) -> str:
        return f"UserRole(user={self.user_id}, role={self.role_id})"
