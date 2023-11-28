from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine
from sqlalchemy.orm import sessionmaker, declarative_base
from src.core.config import get_settings
from sqlalchemy import create_engine

settings = get_settings()

Base = declarative_base()


engine = AsyncEngine(
    create_engine(
        settings.postgres.sqlalchemy_db_uri,
        echo=settings.SQL_ECHO,
        future=True,
    ),
)


async def get_session() -> AsyncSession:
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session
