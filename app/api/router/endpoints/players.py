import uuid
from typing import Any

from fastapi import APIRouter, HTTPException

from app import crud
from app.api.deps import dbSessionDep
from app.models import (
    Message,
    Player,
    PlayerCreate,
    PlayerPublic,
    PlayersPublic,
    PlayerUpdate,
    PlayerPublicCreate,
)
from app.core.config import settings

router = APIRouter()


@router.get("/", response_model=PlayersPublic)
def read_players(skip: int = 0, limit: int = 100) -> Any:
    """
    Retrieve players.
    """

    players = crud.broker.player.get_multi()
    players = players[skip : skip + limit]

    return PlayersPublic(data=players, count=len(players))


@router.get("/{id}", response_model=PlayerPublic)
def read_player(id: uuid.UUID) -> Any:
    """
    Get player by ID.
    """
    player = crud.broker.player.get(id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    return player


@router.post("/", response_model=PlayerPublicCreate)
def create_player(
    *, dbSession: dbSessionDep, player_in: PlayerCreate, secret: str
) -> Any:
    """
    Create new player.
    """
    if secret != settings.MY_SECRET:
        raise HTTPException(status_code=401, detail="You shouldn't try this. Get out of here")

    player = crud.broker.player.get_by_name(name=player_in.name)
    if player:
        raise HTTPException(status_code=403, detail="Player already exist")

    player_create = Player.model_validate(player_in)

    player = crud.db.player.create(
        dbSession, obj_in=player_create
    )
    return player


@router.put("/{id}", response_model=PlayerPublic)
def update_player(
    *,
    dbSession: dbSessionDep,
    id: uuid.UUID,
    player_in: PlayerUpdate,
    secret: str,
) -> Any:
    """
    Update an player.
    """
    if secret != settings.MY_SECRET:
        raise HTTPException(status_code=401, detail="You shouldn't try this. Get out of here")

    player = dbSession.get(Player, id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")

    player = crud.db.player.update(
        dbSession, db_obj=player, obj_in=player_in
    )

    return player


@router.delete("/{id}")
def delete_player(
    dbSession: dbSessionDep, id: uuid.UUID
) -> Message:
    """
    Delete an player.
    """
    player = dbSession.get(Player, id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    player = crud.db.player.delete(dbSession, db_obj=player)
    return Message(message="Player deleted successfully")
