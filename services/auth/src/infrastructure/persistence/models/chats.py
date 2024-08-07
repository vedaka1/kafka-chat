import uuid
from datetime import datetime

from sqlalchemy import TIMESTAMP, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.persistence.models.base import Base


class ChatsModelDB(Base):
    __tablename__ = "chats"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, index=True)
    owner_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    title: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=False), nullable=False
    )


class ChatsMembersModelDB(Base):
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


class ChatRolesModelDB(Base):
    __tablename__ = "chat_roles"

    name: Mapped[str] = mapped_column(primary_key=True, index=True)
