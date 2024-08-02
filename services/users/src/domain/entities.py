import uuid
from dataclasses import dataclass


@dataclass
class User:
    id: uuid.UUID
    username: str
    hashed_password: str
    email: str
    is_active: bool
    is_verified: bool
    is_superuser: bool
