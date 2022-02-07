from typing import Optional

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

from main.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth")


async def get_current_user_id(
        token: str = Depends(oauth2_scheme)
) -> Optional[int]:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, settings.ALGORITHM)
        user_id = payload.get("sub")
    except JWTError:
        return None
    return user_id
