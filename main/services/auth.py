from datetime import datetime, timedelta

from jose import jwt
from passlib.context import CryptContext

from main.config import settings

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def generate_hashed_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_context.verify(plain_password, hashed_password)


def create_access_token(user_id: int) -> str:
    now = datetime.utcnow()
    expired_time = now + timedelta(settings.JWT_EXPIRED_MINUTES)
    payload = {"iat": now, "exp": expired_time, "sub": str(user_id)}
    access_token = jwt.encode(payload, settings.JWT_SECRET_KEY, settings.JWT_ALGORITHM)
    return access_token


def decode_access_token(access_token: str) -> int:
    payload = jwt.decode(access_token, settings.JWT_SECRET_KEY, settings.JWT_ALGORITHM)
    user_id = int(payload.get("sub"))
    return user_id
