import uuid
from typing import TYPE_CHECKING

from sqlmodel import Field, SQLModel
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from typing import ClassVar, List
from sqlalchemy import Column, text
from sqlalchemy.orm import relationship
from sqlmodel import SQLModel, Field

if TYPE_CHECKING:
    from app.models.game import Game


# Shared properties
class PlayerBase(SQLModel):
    name: str = Field(unique=True, index=True, max_length=255)
    is_active: bool = True


# Properties to receive via API on creation
class PlayerCreate(PlayerBase):
    name: str = Field(unique=True, index=True, max_length=255)


class PlayerRegister(SQLModel):
    name: str = Field(unique=True, index=True, max_length=255)


# Properties to receive via API on update, all are optional
class PlayerUpdate(PlayerBase):
    # email: EmailStr | None = Field(default=None, max_length=255)  # type: ignore
    name: str | None = Field(default=None, unique=True, max_length=255)


# Database model, database table inferred from class name
class Player(PlayerBase, table=True):
    __tablename__ = "player"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, sa_column=Column(PG_UUID(as_uuid=True), primary_key=True))
    name: str = Field(max_length=255, nullable=False)
    is_active: bool = Field(nullable=False)
    secret: uuid.UUID = Field(default=text("uuid_generate_v4()"))

    # Relacionamentos (marcados como ClassVar)
    games_as_white: ClassVar[List["Game"]] = relationship(
        "Game", back_populates="player_white_ref", foreign_keys="[Game.player_white]",
    )
    games_as_black: ClassVar[List["Game"]] = relationship(
        "Game", back_populates="player_black_ref", foreign_keys="[Game.player_black]",
    )
    games_as_winner: ClassVar[List["Game"]] = relationship(
        "Game", back_populates="player_winner_ref", foreign_keys="[Game.player_winner]",
    )

    @classmethod
    def from_json(cls, data: dict):
        return cls.model_validate(data)


# Properties to return via API, id is always required
class PlayerPublic(PlayerBase):
    id: uuid.UUID


# Properties to return via API, id is always required
class PlayerPublicCreate(PlayerBase):
    id: uuid.UUID
    secret: uuid.UUID


class PlayersPublic(SQLModel):
    data: list[PlayerPublic]
    count: int


# Generic message
class Message(SQLModel):
    message: str
