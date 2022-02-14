from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from main.api.dependencies.category import get_category_by_id
from main.api.dependencies.database import get_database_session
from main.api.dependencies.item import get_item_by_id
from main.api.exception import ForbiddenException, UnauthorizedException
from main.models.category import CategoryModel
from main.models.item import ItemModel
from main.models.user import UserModel
from main.services.auth import decode_access_token
from main.services.user import get_user_by_id


async def require_authenticated_user(
    session: AsyncSession = Depends(get_database_session),
    http_credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=False)),
) -> UserModel:
    if http_credentials is None:
        raise UnauthorizedException()

    try:
        access_token = http_credentials.credentials
        payload = decode_access_token(access_token)
    except JWTError:
        raise UnauthorizedException()

    user_id = int(payload.get("sub"))
    user = await get_user_by_id(session, user_id)
    if user is None:
        raise UnauthorizedException()

    return user


async def require_permission_on_category(
    user: UserModel = Depends(require_authenticated_user),
    category: CategoryModel = Depends(get_category_by_id),
) -> None:
    if category.user_id != user.id:
        raise ForbiddenException("User does not have permission to perform this action")


async def require_permission_on_item(
    user: UserModel = Depends(require_authenticated_user),
    item: ItemModel = Depends(get_item_by_id),
) -> None:
    if item.user_id != user.id:
        raise ForbiddenException("User does not have permission to perform this action")
