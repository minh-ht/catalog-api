from fastapi import APIRouter

from main.api.routes import category, item, user

api_router = APIRouter()
api_router.include_router(category.router)
api_router.include_router(user.router)
api_router.include_router(item.router)
