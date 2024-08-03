import asyncio
import logging

import orjson
from aiosmtplib import SMTPException
from src.core.container import get_container, init_logger
from src.domain.events import NewUserRegistered
from src.gateways.message_broker.base import BaseMessageConsumer
from src.gateways.smtp.main import BaseSMTPServer


async def send_message(
    message: dict, smtp_server: BaseSMTPServer, logger: logging.Logger
) -> None:
    try:
        await smtp_server.check_connection()
        event = NewUserRegistered(**message)
        message_content = f"{event.message_text} {event.confirmation_link}"
        message = smtp_server.create_message(
            content=message_content, to_address=event.email
        )
        logger.info(f"Sending message to {event.email}")
        await smtp_server.send_email(message=message)
        return None
    except SMTPException as e:
        logger.error(e)


async def main():
    init_logger()
    logger = logging.getLogger()
    container = get_container()
    async with container() as di_container:
        consumer = await di_container.get(BaseMessageConsumer)
        smtp_server = await di_container.get(BaseSMTPServer)
    await consumer.start()
    await smtp_server.start()
    try:
        consumer.consumer.subscribe(topics=["notifications"])
        async for msg in consumer.consumer:
            event = orjson.loads(msg.value)
            await send_message(message=event, smtp_server=smtp_server, logger=logger)
    except Exception as e:
        logger.error(e)
    finally:
        logger.info("Stopping consumer")
        await consumer.stop_consuming()
        await consumer.close()
        logger.info("Stopping smtp server")
        await smtp_server.stop()


if __name__ == "__main__":
    asyncio.run(main())
