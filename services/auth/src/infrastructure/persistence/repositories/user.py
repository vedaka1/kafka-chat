import uuid
from dataclasses import dataclass

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.users.repository import BaseUserRepository
from src.domain.users.user import User


@dataclass
class UserRepository(BaseUserRepository):

    __slots__ = ("session",)
    session: AsyncSession

    async def create(self, user: User) -> None:
        query = text(
            """
                INSERT INTO users (id, username, hashed_password, email, is_active, is_verified, is_superuser)
                VALUES (:id, :username, :hashed_password, :email, :is_active, :is_verified, :is_superuser);
                """
        )
        await self.session.execute(
            query,
            {
                "id": user.id,
                "username": user.username,
                "hashed_password": user.hashed_password,
                "email": user.email,
                "is_active": user.is_active,
                "is_verified": user.is_verified,
                "is_superuser": user.is_superuser,
            },
        )
        return None

    async def update(self, user_id: uuid.UUID, user: User):
        query = text(
            """
                UPDATE users
                SET username = :username, email = :email
                WHERE id = :id;
                """
        )
        await self.session.execute(
            query,
            {
                "id": user_id,
                "username": user.username,
                "email": user.email,
            },
        )
        return None

    async def delete(self, user_id: uuid.UUID) -> None:
        query = text(
            """
                DELETE FROM users
                WHERE id = :id;
                """
        )
        await self.session.execute(
            query,
            {
                "id": user_id,
            },
        )
        return None

    async def _get_by(self, value: uuid.UUID | str, filter: str) -> User | None:
        if filter == "id":
            query = text("""SELECT * FROM users WHERE id = :value;""")
        if filter == "email":
            query = text("""SELECT * FROM users WHERE email = :value;""")
        result = await self.session.execute(query, {"value": value})
        data = result.mappings().one_or_none()
        if data is None:
            return None

        return User(**data)

    async def get_by_id(self, user_id: uuid.UUID) -> User | None:
        return await self._get_by(value=user_id, filter="id")

    async def get_by_email(self, email: str) -> User | None:
        return await self._get_by(value=email, filter="email")

    async def get_all(self, limit: int = 10, offset: int = 0) -> list[User]:
        query = text("""SELECT * FROM users LIMIT :limit OFFSET :offset;""")
        result = await self.session.execute(query, {"limit": limit, "offset": offset})
        data = result.mappings().all()
        return [User(**item) for item in data]

    async def count(self) -> int | None:
        query = text("""SELECT COUNT(*) FROM users;""")
        result = await self.session.execute(query)
        return result.mappings().first()["count"]
