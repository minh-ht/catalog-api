from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from main.api.dependencies.auth import authenticate_user, create_access_token
from main.api.dependencies.get_db import get_db
from main.services.database.user.crud import create_user, get_user_by_email
from main.schemas.user import UserAuth, UserCreate
from main.schemas.token import Token

router = APIRouter()


@router.post("/")
async def register(new_user: UserCreate, db: Session = Depends(get_db)):
    user = get_user_by_email(db, new_user.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This email is already registered"
        )

    create_user(db, new_user)


@router.post("/auth", response_model=Token)
async def auth(user_login: UserAuth, db: Session = Depends(get_db)):
    user = authenticate_user(db, user_login)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Wrong email or password"
        )

    access_token = create_access_token(str(user.id))
    return {"access_token": access_token}