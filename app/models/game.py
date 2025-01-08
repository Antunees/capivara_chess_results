from typing import ClassVar, List, Optional
from sqlalchemy import Column, ForeignKey, String, Boolean, TIMESTAMP, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlmodel import SQLModel, Field

from sqlalchemy import Column, ForeignKey, String, Boolean, TIMESTAMP, text

import uuid
from datetime import datetime

from sqlmodel import Field, Relationship, SQLModel
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from app.models.player import Player


# Shared properties
class GameBase(SQLModel):
    player_white: uuid.UUID | None = Field(default=None)
    player_black: uuid.UUID | None = Field(default=None)
    player_winner: uuid.UUID | None = Field(default='00000000-0000-0000-0000-000000000000')
    start_time: datetime | None = Field(default=None)
    end_time: datetime | None = Field(default=None)


# Properties to receive via API on creation
class GameCreate(GameBase):
    player_white: uuid.UUID = Field(default=None)
    player_black: uuid.UUID = Field(default=None)
    player_winner: uuid.UUID = Field(default='00000000-0000-0000-0000-000000000000')
    start_time: datetime = Field(default=None)
    end_time: datetime = Field(default=None)


# Properties to receive via API on update, all are optional
class GameUpdate(GameBase):
    pass


# Database model, database table inferred from class name
class Game(GameBase, table=True):
    __tablename__ = "game"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, sa_column=Column(PG_UUID(as_uuid=True), primary_key=True))
    player_white: uuid.UUID = Field(sa_column=Column(PG_UUID(as_uuid=True), ForeignKey("player.id"), nullable=False))
    player_black: uuid.UUID = Field(sa_column=Column(PG_UUID(as_uuid=True), ForeignKey("player.id"), nullable=False))
    player_winner: uuid.UUID = Field(sa_column=Column(PG_UUID(as_uuid=True), ForeignKey("player.id"), nullable=False))

    # Relacionamentos (marcados como ClassVar)
    player_white_ref: ClassVar["Player"] = relationship(
        "Player", back_populates="games_as_white", foreign_keys="[Game.player_white]",
        primaryjoin="Game.player_white == Player.id",
        remote_side="Player.id",
    )
    player_black_ref: ClassVar["Player"] = relationship(
        "Player", back_populates="games_as_black", foreign_keys="[Game.player_black]",
        primaryjoin="Game.player_black == Player.id",
        remote_side="Player.id",
    )
    player_winner_ref: ClassVar["Player"] = relationship(
        "Player", back_populates="games_as_winner", foreign_keys="[Game.player_winner]",
        primaryjoin="Game.player_winner == Player.id",
        remote_side="Player.id",
    )


# Properties to return on a list via API, id is always required
class GamePublicFrom(GameBase):
    id: uuid.UUID


# Properties to return via API, id is always required
class GamePublic(GamePublicFrom):
    pass


class GamesPublic(SQLModel):
    data: list[GamePublicFrom]
    count: int
