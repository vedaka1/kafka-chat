import uuid
from dataclasses import dataclass
from datetime import datetime, timedelta


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


@dataclass
class UserConfirmation:
    id: uuid.UUID
    user_id: uuid.UUID
    code: uuid.UUID
    expired_at: datetime
    is_used: bool = False

    @staticmethod
    def create(user_id: uuid.UUID) -> "UserConfirmation":
        return UserConfirmation(
            id=uuid.uuid4(),
            user_id=user_id,
            code=uuid.uuid4(),
            expired_at=datetime.now() + timedelta(minutes=10),
            is_used=False,
        )
