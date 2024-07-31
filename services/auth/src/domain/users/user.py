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

    @staticmethod
    def create(username: str, hashed_password: str, email: str) -> "User":
        return User(
            id=uuid.uuid4(),
            username=username,
            hashed_password=hashed_password,
            email=email,
            is_active=True,
            is_verified=False,
            is_superuser=False,
        )
