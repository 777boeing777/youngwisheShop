from __future__ import annotations
from typing import Sequence, TYPE_CHECKING
from src.core.interfaces import IRepository
from src.apps.company.models import Company
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select, delete
from datetime import datetime

if TYPE_CHECKING:
    from src.apps.company.schemas import CompanyIn


class CompanyRepository(IRepository):
    model = Company

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get(self) -> Sequence[Company]:
        results = await self.session.execute(select(self.model))
        return results.scalars().all()

    async def create(self, in_model: CompanyIn) -> Company:
        company = Company(**in_model.model_dump(), rating=None, updated_at=datetime.now())  # type: ignore[call-arg]
        self.session.add(company)
        await self.session.commit()
        return company

    async def get_by_pk(self, pk: int) -> Company | None:
        company = await self.session.execute(
            select(self.model).where(self.model.id == pk),
        )
        return company.scalar_one_or_none()

    async def get_by_name(self, name: str) -> Company | None:
        company = await self.session.execute(
            select(self.model).where(self.model.name == name),
        )
        return company.scalar_one_or_none()

    async def delete(self) -> None:
        await self.session.execute(delete(self.model))
        await self.session.commit()

    async def delete_by_pk(self, pk: int) -> bool:
        result = await self.session.execute(
            delete(self.model).where(self.model.id == pk),
        )
        await self.session.commit()
        return bool(result.rowcount)
