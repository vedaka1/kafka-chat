import logging
from functools import lru_cache

import aiosmtplib
from aiokafka import AIOKafkaConsumer
from dishka import AsyncContainer, Provider, Scope, make_async_container, provide

from src.core.settings import settings
from src.gateways.message_broker.base import BaseMessageConsumer
from src.gateways.message_broker.broker import KafkaMessageConsumer
from src.gateways.smtp.main import AsyncSMTPServer, BaseSMTPServer


@lru_cache(1)
def init_logger() -> logging.Logger:
    logging.basicConfig(
        # filename="log.log",
        level=logging.INFO,
        encoding="UTF-8",
        format="%(asctime)s %(levelname)s: %(message)s",
    )


class SettingsProvider(Provider):
    @provide(scope=Scope.APP)
    async def app_smtp_server(self) -> BaseSMTPServer:
        return AsyncSMTPServer(
            server=aiosmtplib.SMTP(
                hostname=settings.SMTP.SMTP_HOST,
                port=settings.SMTP.SMTP_PORT,
                username=settings.SMTP.SMTP_EMAIL,
                password=settings.SMTP.SMTP_PASSWORD,
                use_tls=True,
            ),
            from_address=settings.SMTP.SMTP_EMAIL,
            password=settings.SMTP.SMTP_PASSWORD,
            subject=settings.SMTP.SMTP_EMAIL,
        )

    @provide(scope=Scope.APP)
    def consumer(self) -> BaseMessageConsumer:
        return KafkaMessageConsumer(
            consumer=AIOKafkaConsumer(bootstrap_servers=settings.KAFKA_URL),
        )


class UseCasesProvider(Provider):
    scope = Scope.REQUEST


@lru_cache(1)
def get_container() -> AsyncContainer:
    return make_async_container(
        UseCasesProvider(),
        SettingsProvider(),
    )
