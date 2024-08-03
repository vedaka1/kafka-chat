from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import AsyncIterator


@dataclass
class BaseMessageConsumer(ABC):
    @abstractmethod
    async def start_consuming(self, topic: str) -> AsyncIterator[dict]: ...

    @abstractmethod
    async def stop_consuming(self): ...

    @abstractmethod
    async def close(self): ...

    @abstractmethod
    async def start(self): ...
