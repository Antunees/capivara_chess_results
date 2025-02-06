import os
from typing import ClassVar, Literal
from pydantic import BaseModel, field_validator
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlmodel import SQLModel, Field

from sqlalchemy import Column, ForeignKey

import uuid
from datetime import datetime

from sqlmodel import Field, SQLModel
from sqlalchemy.orm import relationship

from app.models.player import Player
import jwt

SECRET_KEY = os.getenv("SECRET_KEY")

# Shared properties
class GameBase(SQLModel):
    player_white: uuid.UUID | None = Field(default=None)
    player_black: uuid.UUID | None = Field(default=None)
    player_winner: uuid.UUID | None = Field(default='00000000-0000-0000-0000-000000000000')
    start_time: datetime | None = Field(default=None)
    end_time: datetime | None = Field(default=None)
    result: Literal['checkmate', 'stalemate', 'insufficient material', '75-move rule', 'fivefold repetition'] | None = Field(max_length=255)
    pgn_text: str | None = Field(default=None)


class RegisterGame(BaseModel):
    token: str

    @field_validator("token")
    def validate_jwt_token(cls, value):
        try:
            # Decodifica o token e valida assinatura e expiração
            jwt.decode(value, SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise ValueError("O token está expirado.")
        except jwt.InvalidTokenError:
            raise ValueError("O token é inválido.")
        return value

# Properties to receive via API on creation
class GameCreate(GameBase):
    id: uuid.UUID = Field(default=None)
    player_white: uuid.UUID = Field(default=None)
    player_black: uuid.UUID = Field(default=None)
    player_winner: uuid.UUID = Field(default='00000000-0000-0000-0000-000000000000')
    start_time: datetime = Field(default=None)
    end_time: datetime = Field(default=None)
    pgn_text: str = Field(default=None)
    result: Literal['checkmate', 'stalemate', 'insufficient material', '75-move rule', 'fivefold repetition'] = Field(max_length=255)


# Properties to receive via API on update, all are optional
class GameUpdate(GameBase):
    pass


# Database model, database table inferred from class name
class Game(GameBase, table=True):
    __tablename__ = "game"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, sa_column=Column(PG_UUID(as_uuid=True), primary_key=True))
    result: str = Field(max_length=255)
    pgn_text: str = Field()
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

    @classmethod
    def from_json(cls, data: dict):
        return cls.model_validate(data)


# Properties to return on a list via API, id is always required
class GamePublicFrom(GameBase):
    id: uuid.UUID


# Properties to return via API, id is always required
class GamePublic(GamePublicFrom):
    pass


class GamesPublic(SQLModel):
    data: list[GamePublicFrom]
    count: int
