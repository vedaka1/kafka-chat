from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from src.api.v1.exc_handlers import init_exc_handlers
from src.api.v1.router import api_router as api_router_v1
from src.core.container import get_container


def init_di(app: FastAPI) -> None:
    container = get_container()
    setup_dishka(container, app)


def create_app():
    app = FastAPI()
    api_v1 = FastAPI()
    init_di(api_v1)
    api_v1.include_router(api_router_v1)
    init_exc_handlers(api_v1)
    app.mount("/api/v1", api_v1)
    return app
