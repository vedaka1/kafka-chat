import logging
from dataclasses import dataclass
from typing import AsyncIterator

import orjson
from aiokafka import AIOKafkaConsumer
from src.gateways.message_broker.base import BaseMessageConsumer

logger = logging.getLogger()


@dataclass
class KafkaMessageConsumer(BaseMessageConsumer):
    consumer: AIOKafkaConsumer

    async def start_consuming(self, topic: str) -> AsyncIterator[dict]:
        self.consumer.subscribe(topics=[topic])

        async for message in self.consumer:
            yield orjson.loads(message.value)

    async def stop_consuming(self):
        self.consumer.unsubscribe()

    async def close(self):
        await self.consumer.stop()

    async def start(self):
        logger.info("Starting consumer")
        await self.consumer.start()
