from typing import Optional

from sqlalchemy.orm import Session

from main.services.auth import generate_hashed_password
from main.models.user import User
from main.schemas.user import UserCreationRequestSchema


def get_user_by_email(session: Session, email: str) -> Optional[User]:
    user = session.query(User).filter_by(email=email).one_or_none()
    return user


async def create_user(session: AsyncSession, email: str, hashed_password: str, full_name: str) -> UserModel:
    user = UserModel(
        email=email,
        hashed_password=hashed_password,
        full_name=full_name,
    )
    session.add(user)
    session.commit()
