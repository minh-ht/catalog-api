from fastapi import APIRouter, Depends, Query, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from main.api.dependencies.auth import require_authenticated_user, require_ownership
from main.api.dependencies.category import require_category
from main.api.dependencies.database import get_database_session
from main.api.dependencies.item import require_item
from main.api.exception import BadRequestException
from main.models.category import CategoryModel
from main.models.item import ItemModel
from main.models.user import UserModel
from main.schemas.item import (
    ItemBatchResponseSchema,
    ItemCreationRequestSchema,
    ItemResponseSchema,
    ItemUpdateRequestSchema,
)
from main.services import item as item_service

router = APIRouter()


@router.post("")
async def create_item(
    create_item_data: ItemCreationRequestSchema,
    session: AsyncSession = Depends(get_database_session),
    category: CategoryModel = Depends(require_category),
    user: UserModel = Depends(require_authenticated_user),
):
    item = await item_service.get_item_by_name(session, create_item_data.name)
    if item:
        raise BadRequestException("Item already exists")
    item = await item_service.create_item(
        session=session,
        name=create_item_data.name,
        description=create_item_data.description,
        category_id=category.id,
        user_id=user.id,
    )
    return JSONResponse(content={"id": item.id}, status_code=status.HTTP_201_CREATED)


@router.get("/{item_id}", response_model=ItemResponseSchema)
async def get_single_item(item: ItemModel = Depends(require_item)):
    return item


@router.get("", response_model=ItemBatchResponseSchema, status_code=status.HTTP_200_OK)
async def get_multiples_items(
    page: int = Query(1, gt=0),
    items_per_page: int = Query(20, gt=0),
    category: CategoryModel = Depends(require_category),
    session: AsyncSession = Depends(get_database_session),
):
    offset = (page - 1) * items_per_page
    items = await item_service.get_items(
        session=session,
        category_id=category.id,
        limit=items_per_page,
        offset=offset,
    )
    total_number_of_items = await item_service.get_total_number_of_items_from_category(session, category.id)
    items_batch_response = ItemBatchResponseSchema(
        total_number_of_items=total_number_of_items,
        items_per_page=items_per_page,
        items=items,
    )
    return items_batch_response


@router.put("/{item_id}", dependencies=[Depends(require_ownership(require_item))])
async def update_item(
    item_update_data: ItemUpdateRequestSchema,
    item: ItemModel = Depends(require_item),
    session: AsyncSession = Depends(get_database_session),
):
    await item_service.update_item(session, item.id, item_update_data.description)
    return JSONResponse(content={}, status_code=status.HTTP_200_OK)


@router.delete("/{item_id}", dependencies=[Depends(require_ownership(require_item))])
async def delete_item(
    item: ItemModel = Depends(require_item),
    session: AsyncSession = Depends(get_database_session),
):
    await item_service.delete_item(session=session, item_id=item.id)
    return JSONResponse(content={}, status_code=status.HTTP_200_OK)
