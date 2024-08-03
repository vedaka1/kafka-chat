from abc import ABC
from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4


@dataclass(frozen=True, kw_only=True)
class BaseMessage(ABC):
    id: UUID = field(default_factory=uuid4)
    occurred_at: datetime = field(default_factory=datetime.now, kw_only=True)
