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

from src.application.services.friends import FriendsService
from src.application.services.user import UserService
from src.application.usecases.create import AddFriendUseCase
from src.application.usecases.delete import DeleteFriendUseCase
from src.application.usecases.get import (
    GetUserFriendsListUseCase,
    GetUsersListUseCase,
    GetUserUseCase,
)
from src.core.settings import settings
from src.domain.users.repository import BaseFriendsRepository
from src.domain.users.service import BaseFriendsService, BaseUserService
from src.gateways.postgresql.database import create_engine, create_session_factory
from src.gateways.postgresql.repositories import (
    BaseUserRepository,
    FriendsRepository,
    UserRepository,
)
from src.gateways.postgresql.transaction import (
    BaseTransactionManager,
    TransactionManager,
)
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
    friends_repository = provide(FriendsRepository, provides=BaseFriendsRepository)


class UseCasesProvider(Provider):
    scope = Scope.REQUEST

    get_users_list = provide(GetUsersListUseCase)
    get_user = provide(GetUserUseCase)
    add_friend = provide(AddFriendUseCase)
    delete_friend = provide(DeleteFriendUseCase)
    get_user_friends_list = provide(GetUserFriendsListUseCase)


class ServiceProvider(Provider):
    scope = Scope.REQUEST

    user_service = provide(UserService, provides=BaseUserService)
    friends_service = provide(FriendsService, provides=BaseFriendsService)


@lru_cache(1)
def get_container() -> AsyncContainer:
    return make_async_container(
        SettingsProvider(),
        DatabaseConfigurationProvider(),
        DatabaseAdaptersProvider(),
        ServiceProvider(),
        SecurityProvider(),
        UseCasesProvider(),
    )
