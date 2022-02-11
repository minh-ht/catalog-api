from typing import Optional

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from main.api.dependencies.category import get_category_by_id
from main.api.dependencies.database import get_database_session
from main.common.exception import NotFoundException
from main.models.category import CategoryModel
from main.models.item import ItemModel
from main.services import item as item_service


async def get_item_by_id(
    item_id: Optional[int] = None,
    category: CategoryModel = Depends(get_category_by_id),
    session: AsyncSession = Depends(get_database_session),
) -> Optional[ItemModel]:
    if item_id is None:
        return None

    item = await item_service.get_item_by_id(session, item_id)
    if item is None:
        raise NotFoundException("Cannot find the specified item")

    if item.category_id != category.id:
        raise NotFoundException("Cannot find the specified item")

    return item
