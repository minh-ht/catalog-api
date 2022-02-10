from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from main.api.dependencies.auth import require_authenticated_user, require_permission_on_category
from main.api.dependencies.category import get_category_by_id
from main.api.dependencies.get_database import get_database_session
from main.common.exception import NoEntityError
from main.models.user import UserModel
from main.schemas.category import CategoryBatchResponseSchema, CategoryCreationRequestSchema, CategoryResponseSchema
from main.services.database import category as category_service

router = APIRouter()


@router.get("/", response_model=List[CategoryBatchResponseSchema], status_code=status.HTTP_200_OK)
async def get_all_categories(session: AsyncSession = Depends(get_database_session)):
    categories = await category_service.get_categories(session)
    return categories


@router.get("/{category_id}", response_model=CategoryResponseSchema, status_code=status.HTTP_200_OK)
async def get_single_category(category: CategoryResponseSchema = Depends(get_category_by_id)):
    return category


@router.post("/")
async def create_category(
    create_category_data: CategoryCreationRequestSchema,
    session: AsyncSession = Depends(get_database_session),
    user: UserModel = Depends(require_authenticated_user),
):
    category = await category_service.get_category_by_name(session, create_category_data.name)
    if category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category name already exists",
        )
    await category_service.create_category(
        session=session,
        name=create_category_data.name,
        description=create_category_data.description,
        user_id=user.id,
    )
    return JSONResponse(content={}, status_code=status.HTTP_201_CREATED)


@router.delete("/{category_id}", dependencies=[Depends(require_permission_on_category)])
async def delete_category(category_id, session: AsyncSession = Depends(get_database_session)):
    try:
        await category_service.delete_category(session, category_id)
    except NoEntityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete the specified category",
        )
    return JSONResponse(content={}, status_code=status.HTTP_200_OK)
