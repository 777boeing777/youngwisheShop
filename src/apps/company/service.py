from __future__ import annotations
from src.core.interfaces import IService
from typing import TYPE_CHECKING, Sequence
from src.apps.company.models import Company

if TYPE_CHECKING:
    from src.apps.company.schemas import CompanyIn
    from src.apps.company.repository import CompanyRepository


class CompanyService(IService):
    model = Company

    def __init__(self, repo: CompanyRepository) -> None:
        self._repo = repo

    async def get(self) -> Sequence[Company]:
        return await self._repo.get()

    async def create(self, in_model: CompanyIn) -> Company:
        return await self._repo.create(in_model=in_model)

    async def get_by_pk(self, pk: int) -> Company | None:
        return await self._repo.get_by_pk(pk=pk)

    async def get_by_name(self, name: str) -> Company | None:
        return await self._repo.get_by_name(name=name)

    async def delete(self) -> None:
        await self._repo.delete()

    async def delete_by_pk(self, pk: int) -> bool:
        return await self._repo.delete_by_pk(pk=pk)
