from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from main.api.dependencies.get_database import get_database_session
from main.models.category import CategoryModel
from main.services.database import category as category_service


async def get_category_by_id(category_id: int, session: AsyncSession = Depends(get_database_session)) -> CategoryModel:
    category = await category_service.get_category_by_id(session, category_id)
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot find the specified category",
        )
    return category
