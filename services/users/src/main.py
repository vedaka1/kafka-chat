from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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
    api_v1.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost"],
        allow_credentials=True,
        allow_methods=["GET", "POST", "HEAD", "OPTIONS", "DELETE", "PUT", "PATCH"],
        allow_headers=[
            "Access-Control-Allow-Headers",
            "Content-Type",
            "Authorization",
            "Access-Control-Allow-Origin",
        ],
    )
    app.mount("/api/v1", api_v1)
    return app
