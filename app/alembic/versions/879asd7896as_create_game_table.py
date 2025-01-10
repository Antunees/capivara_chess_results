"""create game table

Revision ID: 879asd7896as
Revises: 789as7d98aas89d

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "879asd7896as"
down_revision: Union[str, None] = "789as7d98aas89d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "game",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            default=sa.text("uuid_generate_v4()"),
        ),
        sa.Column("result", sa.String(length=255), nullable=False),
        sa.Column("player_white", postgresql.UUID(as_uuid=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["player_white"],
            ["player.id"],
        ),
        sa.Column("player_black", postgresql.UUID(as_uuid=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["player_black"],
            ["player.id"],
        ),
        sa.Column("player_winner", postgresql.UUID(as_uuid=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["player_winner"],
            ["player.id"],
        ),
        sa.Column(
            "start_time",
            sa.TIMESTAMP(timezone=True),
            nullable=True,
        ),
        sa.Column(
            "end_time",
            sa.TIMESTAMP(timezone=True),
            nullable=True,
        ),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            default=sa.text("CURRENT_TIMESTAMP"),
        )
    )

    # op.alter_column("game", "player_white", existing_type=sa.UUID(), nullable=False)
    # op.drop_constraint("game_player_white_fkey", "game", type_="foreignkey")
    # op.create_foreign_key(
    #     None, "game", "player", ["player_white"], ["id"], ondelete="CASCADE"
    # )

    # op.alter_column("game", "player_black", existing_type=sa.UUID(), nullable=False)
    # op.drop_constraint("game_player_black_fkey", "game", type_="foreignkey")
    # op.create_foreign_key(
    #     None, "game", "player", ["player_black"], ["id"], ondelete="CASCADE"
    # )

    # op.alter_column("game", "player_winner", existing_type=sa.UUID(), nullable=True)
    # op.drop_constraint("game_player_winner_fkey", "game", type_="foreignkey")
    # op.create_foreign_key(
    #     None, "game", "player", ["player_winner"], ["id"], ondelete="CASCADE"
    # )


def downgrade() -> None:

    op.drop_constraint(None, "game", type_="foreignkey")
    op.create_foreign_key(
        "game_player_winner_fkey", "game", "player", ["player_winner"], ["id"]
    )
    op.alter_column("game", "player_winner", existing_type=sa.UUID(), nullable=True)
    op.create_foreign_key(
        "game_player_black_fkey", "game", "player", ["player_black"], ["id"]
    )
    op.alter_column("game", "player_black", existing_type=sa.UUID(), nullable=True)
    op.create_foreign_key(
        "game_player_white_fkey", "game", "player", ["player_white"], ["id"]
    )
    op.alter_column("game", "player_white", existing_type=sa.UUID(), nullable=True)

    op.drop_table("game")
