from typing import List, Optional

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from main.models.item import ItemModel


async def get_item_by_id(session: AsyncSession, item_id: int) -> Optional[ItemModel]:
    item = await session.get(ItemModel, item_id)
    return item


async def get_item_by_name(session: AsyncSession, name: str) -> Optional[ItemModel]:
    statement = select(ItemModel).where(ItemModel.name == name)
    result = await session.execute(statement)
    item = result.scalar_one_or_none()
    return item


async def get_items(session: AsyncSession, category_id: int, limit: int, offset: int) -> List[ItemModel]:
    # Config black not to format these block of codes
    # fmt: off
    statement = (
        select(ItemModel)
        .where(ItemModel.category_id == category_id)
        .offset(offset)
        .limit(limit)
    )
    # fmt: on
    result = await session.execute(statement)
    items = result.scalars().all()
    return items


async def create_item(session: AsyncSession, name: str, description: str, category_id: int, user_id: int) -> ItemModel:
    item = ItemModel(
        name=name,
        description=description,
        category_id=category_id,
        user_id=user_id,
    )
    session.add(item)
    await session.commit()
    return item


async def update_item(session: AsyncSession, item_id: int, description: str) -> None:
    item = await session.get(ItemModel, item_id)
    statement = (
        update(ItemModel)
        .where(ItemModel.id == item.id)
        .values(description=description)
        .execution_options(synchronize_session="evaluate")
    )
    await session.execute(statement)
    await session.commit()


async def delete_item(session: AsyncSession, item_id: int) -> None:
    item = await session.get(ItemModel, item_id)
    await session.delete(item)
    await session.commit()
