from sqlalchemy.ext.asyncio import AsyncSession

from main.services.database.session import SessionLocal


async def get_database_session() -> AsyncSession:
    async with SessionLocal() as session:
        yield session
