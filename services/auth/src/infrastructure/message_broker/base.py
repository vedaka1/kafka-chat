from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class BaseMessageBroker(ABC):
    @abstractmethod
    async def start(self): ...

    @abstractmethod
    async def close(self): ...

    @abstractmethod
    async def send_message(self, topic: str, value: bytes, key: bytes): ...
