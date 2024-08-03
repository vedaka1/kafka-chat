import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.persistence.models.base import Base


class UserConfirmationModelDB(Base):
    __tablename__ = "users_confirmation"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE")
    )
    code: Mapped[uuid.UUID] = mapped_column(nullable=False)
    expired_at: Mapped[int] = mapped_column(nullable=False)
    is_used: Mapped[bool] = mapped_column(default=False)
