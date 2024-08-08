from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class Message:
    id: UUID
    chat_id: UUID
    user_id: UUID
    content: str
    created_at: datetime
    updated_at: datetime
