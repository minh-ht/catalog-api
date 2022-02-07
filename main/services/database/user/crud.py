from typing import Optional

from sqlalchemy.orm import Session

from main.services.auth import generate_hashed_password
from main.models.user import User
from main.schemas.user import UserCreationRequestSchema


def get_user_by_email(session: Session, email: str) -> Optional[User]:
    user = session.query(User).filter_by(email=email).one_or_none()
    return user


def create_user(session: Session, user: UserCreationRequestSchema) -> None:
    hashed_password = generate_hashed_password(user.password)
    user = User(
        email=user.email,
        full_name=user.full_name,
        hashed_password=hashed_password
    )
    session.add(user)
    session.commit()
    session.refresh(user)
