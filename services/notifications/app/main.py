import asyncio
import logging

from aiosmtplib import SMTPException
from src.core.container import get_container, init_logger
from src.domain.events import NewUserRegistered
from src.gateways.message_broker.base import BaseMessageConsumer
from src.gateways.smtp.main import BaseSMTPServer


async def send_message(
    message: dict, smtp_server: BaseSMTPServer, logger: logging.Logger
):
    try:
        event = NewUserRegistered(**message)
        message_content = f"{event.message_text} {event.confirmation_link}"
        message = smtp_server.create_message(
            content=message_content, to_address=event.email
        )
        await smtp_server.send_email(message=message)
    except SMTPException as e:
        logger.error(e)


async def main():
    init_logger()
    logger = logging.getLogger()
    container = get_container()
    async with container() as di_container:
        consumer = await di_container.get(BaseMessageConsumer)
        smtp_server = await di_container.get(BaseSMTPServer)
    logger.info("Starting consumer")
    await consumer.start()
    logger.info("Starting smtp server")
    await smtp_server.start()
    try:
        async for msg in consumer.start_consuming("notifications"):
            await send_message(message=msg, smtp_server=smtp_server, logger=logger)
    except Exception as e:
        logger.error(e)
    finally:
        logger.info("Stopping consumer")
        await consumer.stop_consuming()
        await consumer.stop()
        logger.info("Stopping smtp server")
        await smtp_server.stop()


if __name__ == "__main__":
    asyncio.run(main())
