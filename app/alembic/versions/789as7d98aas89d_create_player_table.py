"""create player table

Revision ID: 789as7d98aas89d
Revises:

"""

from typing import Sequence, Union

import sqlalchemy as sa
import sqlmodel.sql.sqltypes
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "789as7d98aas89d"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "player",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            default=sa.text("uuid_generate_v4()")
        ),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column(
            "secret", postgresql.UUID(as_uuid=True), default=sa.text("uuid_generate_v4()")
        ),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            default=sa.text("CURRENT_TIMESTAMP"),
        ),
    )
    op.create_index(op.f("ix_player_secret"), "player", ["secret"])
    op.create_index(op.f("ix_player_name"), "player", ["name"], unique=True)


def downgrade() -> None:
    op.drop_index(op.f("ix_player_secret"), table_name="player")
    op.drop_index(op.f("ix_player_name"), table_name="player")
    op.drop_table("player")
