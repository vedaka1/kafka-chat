"""empty message

Revision ID: c6afab0098c8
Revises: 8187ac903314
Create Date: 2024-08-02 23:47:31.208088

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "c6afab0098c8"
down_revision: Union[str, None] = "8187ac903314"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "users_confirmation",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("code", sa.Uuid(), nullable=False),
        sa.Column("expired_at", sa.Integer(), nullable=False),
        sa.Column("is_used", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_users_confirmation_id"), "users_confirmation", ["id"], unique=False
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_users_confirmation_id"), table_name="users_confirmation")
    op.drop_table("users_confirmation")
    # ### end Alembic commands ###