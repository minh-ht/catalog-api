from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from main.api.dependencies.get_database import get_database_session
from main.schemas.auth import AccessToken
from main.schemas.user import UserAuthenticationRequestSchema, UserCreationRequestSchema
from main.services.auth import create_access_token, verify_password
from main.services.auth import generate_hashed_password
from main.services.user import create_user, get_user_by_email

router = APIRouter()


@router.post("/")
async def register(create_user_data: UserCreationRequestSchema, session: AsyncSession = Depends(get_database_session)):
    user = await get_user_by_email(session, create_user_data.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This email is already registered",
        )
    hashed_password = generate_hashed_password(create_user_data.password)
    await create_user(
        session=session,
        email=create_user_data.email,
        hashed_password=hashed_password,
        full_name=create_user_data.full_name,
    )
    return JSONResponse(content={}, status_code=status.HTTP_201_CREATED)


@router.post("/auth", response_model=AccessToken)
async def authenticate(
    user_authentication_data: UserAuthenticationRequestSchema,
    session: AsyncSession = Depends(get_database_session),
):
    authentication_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid email or password",
    )
    user = await get_user_by_email(session, user_authentication_data.email)
    if user is None:
        raise authentication_error

    if not verify_password(user_authentication_data.password, user.hashed_password):
        raise authentication_error

    access_token = create_access_token(user.id)
    return JSONResponse(content={"access_token": access_token}, status_code=status.HTTP_200_OK)
