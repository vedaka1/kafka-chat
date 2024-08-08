from fastapi import APIRouter

from src.api.v1.views import chats

api_router = APIRouter()
api_router.include_router(chats.router)
