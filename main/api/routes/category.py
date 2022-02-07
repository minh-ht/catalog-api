from typing import List, Optional

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from main.api.dependencies.auth import get_current_user_id
from main.api.dependencies.get_db import get_db_session
from main.schemas.category import CategoryBatchResponseSchema, CategoryCreationRequestSchema, CategoryResponseSchema
from main.services.database import category_crud

router = APIRouter()


@router.get("/", response_model=List[CategoryBatchResponseSchema], status_code=status.HTTP_200_OK)
async def get_all_categories(session: Session = Depends(get_db_session)):
    categories = category_crud.get_categories(session)
    return categories


@router.get("/{category_id}", response_model=CategoryResponseSchema, status_code=status.HTTP_200_OK)
async def get_single_category(category_id, session: Session = Depends(get_db_session)):
    category = category_crud.get_category_by_id(session, category_id)
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cannot find the specified category"
        )
    return category


@router.post("/")
async def create_category(
    create_category_data: CategoryCreationRequestSchema,
    session: Session = Depends(get_db_session),
    user_id: Optional[int] = Depends(get_current_user_id)
):
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User needs to authenticate to create new category"
        )
    if category_crud.get_category_by_name(session, create_category_data.name):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category name already exists"
        )
    category_crud.create_category(session, create_category_data.name, create_category_data.description, user_id)
    return JSONResponse(content={}, status_code=status.HTTP_201_CREATED)


@router.delete("/{category_id}")
async def delete_category(
    category_id,
    session: Session = Depends(get_db_session),
    user_id: Optional[int] = Depends(get_current_user_id)
):
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User needs to authenticate to delete category"
        )

    category = category_crud.get_category_by_id(session, category_id)
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete the specified category"
        )

    if user_id != category.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User does not have permission to delete this category"
        )

    category.delete_category(session, category)
    return JSONResponse(content={}, status_code=status.HTTP_200_OK)
