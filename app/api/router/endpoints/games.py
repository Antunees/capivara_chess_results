import logging
import os
import uuid
from typing import Any

import jwt

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
    RegisterGame,
)

SECRET_KEY = os.getenv("SECRET_KEY")

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
    *, dbSession: dbSessionDep, token_in: RegisterGame
) -> Any:
    """
    Register new game.
    """
    match_info = jwt.decode(token_in.token, SECRET_KEY, algorithms=["HS256"])
    game_in: GameCreate = GameCreate(
        id = match_info['game_id'],
        player_white = match_info['player_white'],
        player_black = match_info['player_black'],
        player_winner = match_info['player_winner'],
        start_time = match_info['start_time'],
        end_time = match_info['end_time'],
        result = match_info['result'],
    )

    if match_info.get('player_winner'):
        game_in.player_winner = match_info['player_winner']
    game_create = Game.model_validate(game_in)


    game = crud.broker.game.get(id=game_in.id)
    if game:
        raise HTTPException(status_code=403, detail="Game already exist")

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
