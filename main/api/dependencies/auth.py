from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from main.api.dependencies.category import get_category_by_id
from main.api.dependencies.database import get_database_session
from main.config import settings
from main.models.category import CategoryModel
from main.models.user import UserModel
from main.services.user import get_user_by_id


async def require_authenticated_user(
    session: AsyncSession = Depends(get_database_session),
    http_authorization_credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=False)),
) -> UserModel:
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User needs to authenticate")
    if http_authorization_credentials is None:
        raise credential_exception

    try:
        token = http_authorization_credentials.credentials
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, settings.JWT_ALGORITHM)
        user_id = int(payload.get("sub"))
    except JWTError:
        raise credential_exception

    user = await get_user_by_id(session, user_id)
    if user is None:
        raise credential_exception

    return user


async def require_permission_on_category(
    user: UserModel = Depends(require_authenticated_user), category: CategoryModel = Depends(get_category_by_id)
) -> None:
    if category.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="User does not have permission to perform this action"
        )
