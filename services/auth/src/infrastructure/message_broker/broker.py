from dataclasses import dataclass

from aiokafka.producer import AIOKafkaProducer

from src.infrastructure.message_broker.base import BaseMessageBroker


@dataclass
class KafkaMessageBroker(BaseMessageBroker):
    producer: AIOKafkaProducer

    async def send_message(self, topic: str, value: bytes, key: bytes):
        await self.producer.send(topic=topic, value=value, key=key)

    async def close(self):
        await self.producer.stop()

    async def start(self):
        await self.producer.start()
