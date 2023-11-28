from __future__ import annotations
from typing import TYPE_CHECKING, Sequence
from fastapi import APIRouter, Depends
from src.apps.company.schemas import CompanyIn, CompanyOut
from src.core.users.auth import current_user
from src.apps.company.depends import company_service
from src.core.exceptions import UniqueConstraintError, NotFoundErrorError
from src.core.http_response_schemas import (
    Unauthorized,
    UniqueConstraint,
    NotFound,
)
from src.core.users.models import User
from fastapi import status

if TYPE_CHECKING:
    from src.apps.company.service import CompanyService

company_router = APIRouter()


@company_router.post(
    "",
    response_model=CompanyOut,
    responses={
        status.HTTP_201_CREATED: {
            "model": CompanyOut,
            "description": "Компания успешно создана",
        },
        status.HTTP_400_BAD_REQUEST: {
            "model": UniqueConstraint,
            "description": "Компания с таким именем уже существует",
        },
        status.HTTP_401_UNAUTHORIZED: {
            "model": Unauthorized,
            "description": "Не авторизированный пользователь не может создать компанию",
        },
    },
    status_code=status.HTTP_201_CREATED,
    description="Зарегистрировать новую компанию",
)
async def register_company(
    company: CompanyIn,
    user: User = Depends(current_user),
    service: CompanyService = Depends(company_service),
) -> CompanyOut:
    if await service.get_by_name(name=company.name):
        raise UniqueConstraintError(
            detail="Компания с названием <%s> уже зарегистрирована в системе"
            % company.name,
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    return await service.create(in_model=company)


@company_router.get(
    "",
    response_model=Sequence[CompanyOut],
    description="Получить все компании",
    status_code=status.HTTP_200_OK,
)
async def companies_list(
    service: CompanyService = Depends(company_service),
) -> Sequence[CompanyOut]:
    return await service.get()


@company_router.delete(
    "",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Удалить все компании",
)
async def delete_companies(service: CompanyService = Depends(company_service)):
    await service.delete()


@company_router.get(
    "/{pk}/",
    status_code=status.HTTP_200_OK,
    description="Детальное представление компании",
    responses={
        status.HTTP_200_OK: {
            "model": CompanyOut,
            "description": "Детальное представление компании",
        },
        status.HTTP_404_NOT_FOUND: {
            "model": NotFound,
            "description": "Компания не найдена",
        },
    },
)
async def company_detail(
    pk: int,
    service: CompanyService = Depends(company_service),
) -> CompanyOut:
    company = await service.get_by_pk(pk=pk)
    if not company:
        raise NotFoundErrorError(
            detail="Компания с идентификатором %s не была найдена" % pk,
            status_code=404,
        )
    return company


@company_router.delete(
    "/{pk}/",
    description="Удалить компанию",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_204_NO_CONTENT: {"description": "Компания успешно удалена"},
        status.HTTP_404_NOT_FOUND: {
            "model": NotFound,
            "description": "Компания не найдена",
        },
    },
)
async def delete_company(pk: int, service: CompanyService = Depends(company_service)):
    is_deleted = await service.delete_by_pk(pk=pk)
    if not is_deleted:
        raise NotFoundErrorError(
            detail="Объект с идентификатором %s не был найден" % pk,
            status_code=404,
        )
