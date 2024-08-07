import logging.handlers
from contextlib import asynccontextmanager

from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.infrastructure.di.container import get_container, init_logger
from src.infrastructure.message_broker.base import BaseMessageBroker
from src.presentation.api.v1.router import api_router as api_router_v1
from src.presentation.exc_handlers import init_exc_handlers


def init_di(app: FastAPI) -> None:
    container = get_container()
    setup_dishka(container, app)


def init_routers(app: FastAPI):
    app.include_router(api_router_v1)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger = logging.getLogger()
    logger.info("Starting broker...")
    container = get_container()
    async with container() as di_container:
        broker = await di_container.get(BaseMessageBroker)
        try:
            await broker.start()
        except Exception as e:
            logger.error(f"Failed to start broker: {e}")
            raise e
    yield
    async with container() as di_container:
        broker = await di_container.get(BaseMessageBroker)
        logger.info("Stoping broker...")
        await broker.close()


def create_app() -> FastAPI:
    init_logger()
    app = FastAPI(
        lifespan=lifespan,
    )
    api_v1 = FastAPI(
        title="NeuroMesh v1",
        description="NeuroMesh REST API v1",
        # debug=True,
        # lifespan=lifespan,
    )
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
    init_di(api_v1)
    init_routers(api_v1)
    init_exc_handlers(api_v1)
    # handler = init_loki_logger(app_name="api")
    # logging.getLogger().addHandler(handler)
    # logging.getLogger("uvicorn.access").addHandler(handler)
    app.mount("/api/v1", api_v1)
    return app
