from sqlalchemy.orm import Session

from main.services.database.session import SessionLocal


class DatabaseContextManager:
    def __init__(self):
        self.db = SessionLocal()

    def __enter__(self):
        return self.db

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db.close()


async def get_db_session() -> Session:
    with DatabaseContextManager() as db:
        yield db
