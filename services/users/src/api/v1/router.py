from fastapi import APIRouter

from src.api.v1.views import friends, users

api_router = APIRouter()
# api_router.include_router(friends.router)
api_router.include_router(
    users.router,
)
