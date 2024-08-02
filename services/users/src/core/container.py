import logging
import logging.handlers
from functools import lru_cache
from typing import AsyncGenerator

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

from src.core.settings import settings
from src.domain.use_cases import GetUsersListUseCase, GetUserUseCase
from src.gateways.postgresql.database import create_engine, create_session_factory
from src.gateways.postgresql.repositories import BaseUserRepository, UserRepository
from src.gateways.postgresql.transaction import (
    BaseTransactionManager,
    TransactionManager,
)
from src.services.user import UserService
from src.utils.id_provider import BaseIdProvider, JwtTokenIdProvider
from src.utils.jwt_processor import BaseJwtTokenProcessor, JwtTokenProcessor


@lru_cache(1)
def init_logger() -> None:
    logging.basicConfig(
        # filename="log.log",
        level=logging.INFO,
        encoding="UTF-8",
        format="%(asctime)s %(levelname)s: %(message)s",
    )
    return None


class SettingsProvider(Provider):
    @provide(scope=Scope.APP)
    def engine(self) -> AsyncEngine:
        return create_engine()

    @provide(scope=Scope.APP)
    def session_factory(self, engine: AsyncEngine) -> async_sessionmaker:
        return create_session_factory(engine)


class SecurityProvider(Provider):
    jwt_processor = provide(
        JwtTokenProcessor, provides=BaseJwtTokenProcessor, scope=Scope.APP
    )


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


class UseCasesProvider(Provider):
    scope = Scope.REQUEST

    get_users_list = provide(GetUsersListUseCase)
    get_user = provide(GetUserUseCase)


class ServiceProvider(Provider):
    scope = Scope.REQUEST

    user_service = provide(UserService)


@lru_cache(1)
def get_container() -> AsyncContainer:
    return make_async_container(
        SettingsProvider(),
        DatabaseConfigurationProvider(),
        DatabaseAdaptersProvider(),
        UseCasesProvider(),
        SecurityProvider(),
        ServiceProvider(),
    )
