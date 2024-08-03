import logging
import logging.handlers
from functools import lru_cache
from multiprocessing import Queue
from typing import AsyncGenerator

import logging_loki
from aiokafka import AIOKafkaProducer
from dishka import (
    AsyncContainer,
    Provider,
    Scope,
    from_context,
    make_async_container,
    provide,
)
from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from src.application.common.id_provider import BaseIdProvider
from src.application.common.jwt_processor import BaseJwtTokenProcessor
from src.application.common.password_hasher import BasePasswordHasher
from src.application.common.transaction import BaseTransactionManager
from src.application.usecases.auth import *
from src.application.usecases.auth.login import LoginUseCase
from src.application.usecases.users import *
from src.domain.users.repository import (
    BaseUserConfirmationRepository,
    BaseUserRepository,
)
from src.infrastructure.authentication.id_provider import JwtTokenIdProvider
from src.infrastructure.authentication.jwt_processor import JwtTokenProcessor
from src.infrastructure.authentication.password_hasher import PasswordHasher
from src.infrastructure.config import settings
from src.infrastructure.message_broker.base import BaseMessageBroker
from src.infrastructure.message_broker.broker import KafkaMessageBroker
from src.infrastructure.persistence.main import create_engine, create_session_factory
from src.infrastructure.persistence.repositories import UserRepository
from src.infrastructure.persistence.repositories.user import UserConfirmationRepository
from src.infrastructure.persistence.transaction import TransactionManager


@lru_cache(1)
def init_logger() -> None:
    logging.basicConfig(
        # filename="log.log",
        level=logging.INFO,
        encoding="UTF-8",
        format="%(asctime)s %(levelname)s: %(message)s",
    )
    return None


@lru_cache(1)
def init_loki_logger(app_name: str = "app"):
    return logging_loki.LokiQueueHandler(
        Queue(-1),
        url="http://loki:3100/loki/api/v1/push",
        tags={"application": app_name},
        version="1",
    )


class SettingsProvider(Provider):
    @provide(scope=Scope.APP)
    def engine(self) -> AsyncEngine:
        return create_engine()

    @provide(scope=Scope.APP)
    def session_factory(self, engine: AsyncEngine) -> async_sessionmaker:
        return create_session_factory(engine)

    @provide(scope=Scope.APP)
    def broker(self) -> BaseMessageBroker:
        return KafkaMessageBroker(
            producer=AIOKafkaProducer(bootstrap_servers=settings.KAFKA_URL),
        )


class SecurityProvider(Provider):
    request = from_context(
        scope=Scope.REQUEST,
        provides=Request,
    )
    password_hasher = provide(
        PasswordHasher, provides=BasePasswordHasher, scope=Scope.APP
    )
    jwt_processor = provide(
        JwtTokenProcessor, provides=BaseJwtTokenProcessor, scope=Scope.APP
    )

    @provide(scope=Scope.REQUEST, provides=BaseIdProvider)
    def id_provider(
        self, token_processor: BaseJwtTokenProcessor, request: Request
    ) -> BaseIdProvider:
        return JwtTokenIdProvider(token_processor=token_processor, token=request.auth)


class DatabaseConfigurationProvider(Provider):
    @provide(scope=Scope.REQUEST, provides=AsyncSession)
    async def provide_db_connection(
        self, session_factory: async_sessionmaker
    ) -> AsyncGenerator[AsyncSession, None]:
        session: AsyncSession = session_factory()
        yield session
        await session.close()


class DatabaseAdaptersProvider(Provider):
    scope = Scope.REQUEST

    unit_of_work = provide(TransactionManager, provides=BaseTransactionManager)
    user_repository = provide(UserRepository, provides=BaseUserRepository)
    user_confirmation_repository = provide(
        UserConfirmationRepository, provides=BaseUserConfirmationRepository
    )


class UseCasesProvider(Provider):
    scope = Scope.REQUEST

    get_users_list = provide(GetUsersListUseCase)
    register = provide(RegisterUseCase)
    login = provide(LoginUseCase)
    confirmation = provide(UserConfirmationUseCase)


@lru_cache(1)
def get_container() -> AsyncContainer:
    return make_async_container(
        SettingsProvider(),
        DatabaseConfigurationProvider(),
        DatabaseAdaptersProvider(),
        UseCasesProvider(),
        SecurityProvider(),
    )
