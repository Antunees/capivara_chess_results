from fastapi import APIRouter

from app.api.router.endpoints import games, players, utils

api_router = APIRouter()

api_router.include_router(players.router, prefix="/players", tags=["players"])
api_router.include_router(games.router, prefix="/games", tags=["games"])
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
