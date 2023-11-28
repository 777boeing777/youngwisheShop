from typing import Optional
from fastapi_users import models
from fastapi_users import schemas
from pydantic import EmailStr
from datetime import datetime


class UserRead(schemas.BaseUser[int]):
    id: models.ID
    email: EmailStr
    joined_at: datetime
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    middle_name: Optional[str] = None
    last_login: Optional[datetime] = None


class UserCreate(schemas.BaseUserCreate):
    email: EmailStr
    password: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    middle_name: Optional[str] = None


class UserUpdate(schemas.BaseUserUpdate):
    password: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None
    is_verified: Optional[bool] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    middle_name: Optional[str] = None
    last_login: Optional[datetime] = None
