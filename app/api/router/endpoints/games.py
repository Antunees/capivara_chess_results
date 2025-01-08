import uuid
from typing import Any

from fastapi import APIRouter, HTTPException

from app import crud
from app.api.deps import dbSessionDep
from app.models import (
    Message,
    Game,
    GameCreate,
    GamePublic,
    GamesPublic,
    GameUpdate,
)

router = APIRouter()


@router.get("/", response_model=GamesPublic)
def read_games(skip: int = 0, limit: int = 100) -> Any:
    """
    Retrieve games.
    """

    games = crud.broker.game.get_multi()
    games = games[skip : skip + limit]

    return GamesPublic(data=games, count=len(games))


@router.get("/{id}", response_model=GamePublic)
def read_game(id: uuid.UUID) -> Any:
    """
    Get game by ID.
    """
    game = crud.broker.game.get(id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    return game


@router.post("/", response_model=GamePublic)
def register_game(
    *, dbSession: dbSessionDep, game_in: GameCreate
) -> Any:
    """
    Register new game.
    """
    game_create = Game.model_validate(game_in)

    game = crud.db.game.create(
        dbSession, obj_in=game_create
    )
    return game


@router.put("/{id}", response_model=GamePublic)
def update_game(
    *,
    dbSession: dbSessionDep,
    id: uuid.UUID,
    game_in: GameUpdate,
) -> Any:
    """
    Update an game.
    """
    game = dbSession.get(Game, id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    game = crud.db.game.update(
        dbSession, db_obj=game, obj_in=game_in
    )

    return game


@router.delete("/{id}")
def delete_game(
    dbSession: dbSessionDep, id: uuid.UUID
) -> Message:
    """
    Delete an game.
    """
    game = dbSession.get(Game, id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    game = crud.db.game.delete(dbSession, db_obj=game)
    return Message(message="Game deleted successfully")
