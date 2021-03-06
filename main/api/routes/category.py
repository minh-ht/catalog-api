from typing import Dict, List

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from main.api.dependencies.auth import require_authenticated_user, require_ownership
from main.api.dependencies.category import require_category
from main.api.dependencies.database import get_database_session
from main.api.exception import BadRequestException
from main.models.category import CategoryModel
from main.models.user import UserModel
from main.schemas.category import (
    CategoryBatchResponseSchema,
    CategoryCreationRequestSchema,
    CategoryResponseSchema,
)
from main.services import category as category_service

router = APIRouter()


@router.get("", response_model=List[CategoryBatchResponseSchema], status_code=status.HTTP_200_OK)
async def get_all_categories(session: AsyncSession = Depends(get_database_session)):
    categories = await category_service.get_categories(session)
    return categories


@router.get("/{category_id}", response_model=CategoryResponseSchema, status_code=status.HTTP_200_OK)
async def get_single_category(category: CategoryResponseSchema = Depends(require_category)):
    return category


@router.post("", response_model=Dict[str, int])
async def create_category(
    create_category_data: CategoryCreationRequestSchema,
    session: AsyncSession = Depends(get_database_session),
    user: UserModel = Depends(require_authenticated_user),
):
    category = await category_service.get_category_by_name(session, create_category_data.name)
    if category:
        raise BadRequestException("Category already exists")
    category = await category_service.create_category(
        session=session,
        name=create_category_data.name,
        description=create_category_data.description,
        user_id=user.id,
    )
    return JSONResponse(content={"id": category.id}, status_code=status.HTTP_201_CREATED)


@router.delete("/{category_id}")
async def delete_category(
    category: CategoryModel = Depends(require_ownership(require_category)),
    session: AsyncSession = Depends(get_database_session),
):
    await category_service.delete_category(session=session, category_id=category.id)
    return JSONResponse(content={}, status_code=status.HTTP_200_OK)
