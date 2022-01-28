from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session

from main.api.dependencies import auth
from main.models.user import User
from main.schemas.user import UserCreate


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    user = db.query(User).filter_by(email=email).first()
    return user


def create_user(db: Session, user: UserCreate) -> None:
    hashed_password = auth.get_hashed_password(user.password)
    db_user = User(
        email=user.email,
        full_name=user.full_name,
        hashed_password=hashed_password,
        created=datetime.now()
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
