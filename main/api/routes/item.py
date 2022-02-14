from typing import List

from fastapi import APIRouter, Depends, Query, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from main.api.dependencies.auth import (
    require_authenticated_user,
    require_permission_on_item,
)
from main.api.dependencies.category import get_category_by_id
from main.api.dependencies.database import get_database_session
from main.api.dependencies.item import get_item_by_id
from main.common.exception import BadRequestException
from main.models.category import CategoryModel
from main.models.item import ItemModel
from main.models.user import UserModel
from main.schemas.item import (
    ItemCreationRequestSchema,
    ItemResponseSchema,
    ItemUpdateRequestSchema,
)
from main.services import item as item_service

router = APIRouter()


@router.post("/items")
async def create_item(
    create_item_data: ItemCreationRequestSchema,
    session: AsyncSession = Depends(get_database_session),
    category: CategoryModel = Depends(get_category_by_id),
    user: UserModel = Depends(require_authenticated_user),
):
    item = await item_service.get_item_by_name(session, create_item_data.name)
    if item:
        raise BadRequestException("Item name already exists")
    await item_service.create_item(
        session=session,
        name=create_item_data.name,
        description=create_item_data.description,
        category_id=category.id,
        user_id=user.id,
    )
    return JSONResponse(content={}, status_code=status.HTTP_201_CREATED)


@router.get("/items/{item_id}", response_model=ItemResponseSchema)
async def get_single_item(item: ItemModel = Depends(get_item_by_id)):
    return item


@router.get("/items", response_model=List[ItemResponseSchema], status_code=status.HTTP_200_OK)
async def get_multiples_items(
    page: int = Query(1, gt=0),
    items_per_page: int = Query(20, gt=0),
    category: CategoryModel = Depends(get_category_by_id),
    session: AsyncSession = Depends(get_database_session),
):
    items = await item_service.get_items(
        session=session,
        category_id=category.id,
        page=page,
        items_per_page=items_per_page,
    )
    return items


@router.put("/items/{item_id}", response_model=ItemResponseSchema, dependencies=[Depends(require_permission_on_item)])
async def update_item(
    item_update_data: ItemUpdateRequestSchema,
    item: ItemModel = Depends(get_item_by_id),
    session: AsyncSession = Depends(get_database_session),
):
    await item_service.update_item(session, item.id, item_update_data.description)
    return JSONResponse(content={}, status_code=status.HTTP_200_OK)


@router.delete(
    "/items/{item_id}",
    response_model=ItemResponseSchema,
    dependencies=[Depends(require_permission_on_item)],
)
async def delete_item(
    item: ItemModel = Depends(get_item_by_id),
    session: AsyncSession = Depends(get_database_session),
):
    await item_service.delete_item(session=session, item_id=item.id)
    return JSONResponse(content={}, status_code=status.HTTP_200_OK)
