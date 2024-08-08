import uuid
from datetime import datetime

from sqlalchemy import TIMESTAMP, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    is_verified: Mapped[bool] = mapped_column(default=False)
    is_superuser: Mapped[bool] = mapped_column(default=False)


class ChatModel(Base):
    __tablename__ = "chats"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, index=True)
    owner_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    title: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=False), nullable=False
    )


class ChatsMembersModel(Base):
    __tablename__ = "chats_members"

    id: Mapped[int] = mapped_column(primary_key=True)
    chat_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("chats.id", ondelete="CASCADE"), nullable=False, index=True
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    joined_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=False), nullable=False
    )
    role: Mapped[str] = mapped_column(
        ForeignKey("chat_roles.name", ondelete="CASCADE"), nullable=False
    )


class ChatRolesModel(Base):
    __tablename__ = "chat_roles"

    name: Mapped[str] = mapped_column(primary_key=True, index=True)


class MessagesModelDB(Base):
    __tablename__ = "messages"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, index=True)
    chat_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("chats.id", ondelete="CASCADE"), nullable=False
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    content: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=False), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=False), nullable=True
    )
