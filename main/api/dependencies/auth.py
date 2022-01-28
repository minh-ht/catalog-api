from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from main.config import settings
from main.models.user import User
from main.services.database.user.crud import get_user_by_email
from main.schemas.user import UserAuth

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth")


def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_context.verify(plain_password, hashed_password)


def create_access_token(
        subject: str, expires_delta: Optional[timedelta] = None
) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = (datetime.utcnow()
                  + timedelta(settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode = {"exp": expire, "sub": subject}
    encoded_jwt = jwt.encode(to_encode,
                             settings.SECRET_KEY,
                             settings.ALGORITHM)
    return encoded_jwt


def authenticate_user(
        db: Session, user_login: UserAuth
) -> Optional[User]:
    user = get_user_by_email(db, user_login.email)
    if not user:
        return None

    if not verify_password(user_login.password, user.hashed_password):
        return None

    return user


async def get_current_user_id(token: str = Depends(oauth2_scheme)) -> int:
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
        user_id = payload.get("sub")
    except JWTError:
        raise credential_exception
    return user_id
