from __future__ import annotations
from typing import AsyncGenerator, TYPE_CHECKING

import pytest

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text

from src.main import app
from src.tests import defaults
from src.core.config import get_settings
from src.core.sql.database import Base, get_session
from src.core.users.models import User
from src.core.users.schemas import UserCreate

from httpx import AsyncClient
from src.core.users.manager import UserManager
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncEngine
    from src.main import YshopAPI

settings = get_settings(db_only=True)

async_engine = create_async_engine(settings.sqlalchemy_db_uri)


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture(scope="session")
async def async_engine_test() -> AsyncGenerator[AsyncEngine]:
    async with async_engine.connect() as connection:
        await connection.execute(text("COMMIT;"))
        await connection.execute(text(f"CREATE DATABASE {defaults.TEST_DB_NAME};"))
    yield create_async_engine(defaults.SQLALCHEMY_DATABASE_TEST_URI)
    async with async_engine.connect() as connection:
        await connection.execute(text("COMMIT;"))
        await connection.execute(text(f"DROP DATABASE {defaults.TEST_DB_NAME};"))


@pytest.fixture(scope="session")
async def bind(async_engine_test: AsyncEngine) -> AsyncGenerator[AsyncEngine]:
    async with async_engine_test.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    yield async_engine_test
    async with async_engine_test.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
    await async_engine_test.dispose()


@pytest.fixture(scope="session")
def async_session_class(bind: AsyncEngine) -> sessionmaker[AsyncSession]:
    return sessionmaker(
        bind=bind,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
    )


@pytest.fixture(scope="session")
def test_app(async_session_class: sessionmaker[AsyncSession]) -> YshopAPI:
    async def get_test_session():
        async with async_session_class() as session:
            yield session

    app.dependency_overrides[get_session] = get_test_session
    return app


@pytest.fixture
async def session(
    async_session_class: sessionmaker[AsyncSession],
) -> AsyncGenerator[AsyncSession]:
    async with async_session_class() as session:
        await session.begin()
        yield session
        await session.rollback()
        for table in reversed(Base.metadata.sorted_tables):
            await session.execute(text(f"TRUNCATE {table.name} CASCADE;"))
            await session.commit()


@pytest.fixture
async def get_test_user_db(
    session: AsyncSession,
) -> AsyncGenerator[SQLAlchemyUserDatabase]:
    yield SQLAlchemyUserDatabase(session, User)


@pytest.fixture
async def get_test_user_manager(
    get_test_user_db: SQLAlchemyUserDatabase,
) -> AsyncGenerator[UserManager]:
    yield UserManager(get_test_user_db)


@pytest.fixture
def async_client(test_app: YshopAPI, session: AsyncSession) -> AsyncClient:
    """Фикстура session необходима для очистки бд"""
    return AsyncClient(app=test_app, base_url=defaults.HOST_URL)


@pytest.fixture
def get_test_user_data() -> dict:
    return {
        "email": defaults.TEST_USER_EMAIL,
        "first_name": defaults.TEST_USER_FIRST_NAME,
        "last_name": defaults.TEST_USER_LAST_NAME,
        "middle_name": defaults.TEST_USER_MIDDLE_NAME,
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,
        "password": defaults.TEST_USER_PASSWORD,
    }


@pytest.fixture
async def create_test_user(
    session: AsyncSession,
    get_test_user_data: dict,
    get_test_user_manager: UserManager,
) -> User:
    create_user_schema = UserCreate(**get_test_user_data)
    user = await get_test_user_manager.create(create_user_schema, safe=True)
    return user
