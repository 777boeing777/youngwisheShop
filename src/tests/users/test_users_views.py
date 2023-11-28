from __future__ import annotations
from typing import TYPE_CHECKING
import pytest
from fastapi import status
from src.tests import defaults

if TYPE_CHECKING:
    from httpx import AsyncClient
    from src.main import YshopAPI
    from src.core.users.models import User
    from sqlalchemy.ext.asyncio import AsyncSession


@pytest.mark.anyio
async def test_register_view(
    async_client: AsyncClient,
    test_app: YshopAPI,
    get_test_user_data: dict,
):
    """Тест на регистрацию пользователя"""
    url = test_app.url_path_for("register:register")
    async with async_client as client:
        response = await client.post(url, json=get_test_user_data)
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.anyio
async def test_auth_view(
    async_client: AsyncClient,
    test_app: YshopAPI,
    create_test_user: User,
    session: AsyncSession,
):
    """Тест на авторизацию пользователя (в том числе проставление поля last_login)"""
    assert create_test_user.last_login is None

    url = test_app.url_path_for("auth:jwt.login")
    async with async_client as client:
        response = await client.post(
            url,
            data={
                "username": defaults.TEST_USER_EMAIL,
                "password": defaults.TEST_USER_PASSWORD,
            },
        )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["access_token"]

    await session.refresh(create_test_user)
    assert create_test_user.last_login
