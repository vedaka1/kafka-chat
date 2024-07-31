import uuid
from dataclasses import dataclass


@dataclass
class UserOut:
    id: uuid.UUID
    username: str
    email: str
    is_active: bool
    is_verified: bool
    is_superuser: bool
