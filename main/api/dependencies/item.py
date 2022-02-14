from typing import Optional

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from main.api.dependencies.category import require_category
from main.api.dependencies.database import get_database_session
from main.api.exception import NotFoundException
from main.models.category import CategoryModel
from main.models.item import ItemModel
from main.services import item as item_service


async def require_item(
    item_id: int,
    category: CategoryModel = Depends(require_category),
    session: AsyncSession = Depends(get_database_session),
) -> Optional[ItemModel]:
    item = await item_service.get_item_by_id(session, item_id)
    if item is None:
        raise NotFoundException("Cannot find the specified item")

    if item.category_id != category.id:
        raise NotFoundException("Cannot find the specified item")

    return item
