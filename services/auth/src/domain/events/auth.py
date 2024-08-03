from dataclasses import dataclass
from typing import ClassVar

from src.domain.events.base import BaseEvent


@dataclass
class NewUserRegistered(BaseEvent):
    event_title: ClassVar[str] = "New user registered"
    email: str
    confirmation_link: str
