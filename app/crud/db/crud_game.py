import app.crud.broker.crud_game as crud_game
from app.crud.db.base import CRUDBase
from app.models.game import Game, GameCreate, GameUpdate


class CRUDGame(CRUDBase[Game, GameCreate, GameUpdate, crud_game.CRUDGame]):
   pass


game = CRUDGame(Game, crud_game.CRUDGame)
