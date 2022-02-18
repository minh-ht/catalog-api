from fastapi import APIRouter

from main.api.routes import category, item, user

api_router = APIRouter()
api_router.include_router(category.router, prefix="/categories", tags=["categories"])
api_router.include_router(item.router, prefix="/categories/{category_id}/items", tags=["items"])
api_router.include_router(user.router, prefix="/users", tags=["users"])
