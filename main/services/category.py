from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from main.common.exception import NoEntityException
from main.models.category import CategoryModel


async def get_category_by_id(session: AsyncSession, category_id: int) -> Optional[CategoryModel]:
    category = await session.get(CategoryModel, category_id)
    return category


async def get_category_by_name(session: AsyncSession, name: str) -> Optional[CategoryModel]:
    statement = select(CategoryModel).where(CategoryModel.name == name)
    result = await session.execute(statement)
    category = result.scalar_one_or_none()
    return category


async def get_categories(session: AsyncSession) -> List[CategoryModel]:
    statement = select(CategoryModel)
    result = await session.execute(statement)
    categories = result.scalars().all()
    return categories


async def create_category(session: AsyncSession, name: str, description: str, user_id: int) -> CategoryModel:
    category = CategoryModel(name=name, description=description, user_id=user_id)
    session.add(category)
    await session.commit()
    return category


async def delete_category(session: AsyncSession, category_id: int) -> None:
    category = await session.get(CategoryModel, category_id)
    if category is None:
        raise NoEntityException
    await session.delete(category)
    await session.commit()
