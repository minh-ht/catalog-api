from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from main.models.user import UserModel


async def get_user_by_id(session: AsyncSession, user_id: int) -> Optional[UserModel]:
    user = await session.get(UserModel, user_id)
    return user


async def get_user_by_email(session: AsyncSession, email: str) -> Optional[UserModel]:
    statement = select(UserModel).where(UserModel.email == email)
    result = await session.execute(statement)
    user = result.scalar_one_or_none()
    return user


async def create_user(session: AsyncSession, email: str, hashed_password: str, full_name: str) -> UserModel:
    user = UserModel(
        email=email,
        hashed_password=hashed_password,
        full_name=full_name,
    )
    session.add(user)
    await session.commit()
    return user
