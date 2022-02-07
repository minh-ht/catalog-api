from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from main.api.dependencies.get_db import get_db_session
from main.models.user import User
from main.schemas.user import (
    UserAuthenticationRequestSchema,
    UserCreationRequestSchema
)
from main.schemas.token import AccessToken
from main.services.auth import create_access_token, verify_password
from main.services.database.user.crud import create_user, get_user_by_email

router = APIRouter()


def authenticate_user(
        db: Session, user_login: UserAuthenticationRequestSchema
) -> Optional[User]:
    user = get_user_by_email(db, user_login.email)
    if not user:
        return None

    if not verify_password(user_login.password, user.hashed_password):
        return None

    return user


@router.post("/")
async def register(
        create_user_data: UserCreationRequestSchema,
        db: Session = Depends(get_db_session)
):
    user = get_user_by_email(db, create_user_data.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This email is already registered"
        )

    create_user(db, create_user_data)
    return JSONResponse(content={}, status_code=status.HTTP_201_CREATED)


@router.post("/auth", response_model=AccessToken)
async def auth(
        user_login: UserAuthenticationRequestSchema,
        db: Session = Depends(get_db_session)
):
    user = authenticate_user(db, user_login)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    access_token = create_access_token(user.id)
    return JSONResponse(content={"access_token": access_token},
                        status_code=status.HTTP_200_OK)
