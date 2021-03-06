from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from main.api.dependencies.database import get_database_session
from main.api.exception import NotFoundException
from main.models.category import CategoryModel
from main.services import category as category_service


async def require_category(category_id: int, session: AsyncSession = Depends(get_database_session)) -> CategoryModel:
    category = await category_service.get_category_by_id(session, category_id)
    if category is None:
        raise NotFoundException("Cannot find the specified category")
    return category
