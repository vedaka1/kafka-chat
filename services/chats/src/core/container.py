import logging
import logging.handlers
from functools import lru_cache
from typing import AsyncGenerator

from dishka import AsyncContainer, Provider, Scope, make_async_container, provide
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from src.application.services.chat import ChatService
from src.application.usecases.create import CreateChatUseCase
from src.application.usecases.get import GetChatsListUseCase
from src.domain.chats.repository import BaseChatRepository
from src.domain.chats.service import BaseChatService
from src.gateways.postgresql.database import create_engine, create_session_factory
from src.gateways.postgresql.repositories import ChatRepository
from src.gateways.postgresql.transaction import (
    BaseTransactionManager,
    TransactionManager,
)
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
    chat_repository = provide(ChatRepository, provides=BaseChatRepository)


class UseCasesProvider(Provider):
    scope = Scope.REQUEST

    get_chats_list = provide(GetChatsListUseCase)
    create_chat = provide(CreateChatUseCase)


class ServiceProvider(Provider):
    scope = Scope.REQUEST

    chat_service = provide(ChatService, provides=BaseChatService)


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
