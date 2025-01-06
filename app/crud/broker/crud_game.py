from app.crud.broker.base import BrokerBase
from app.models.game import Game, GameCreate, GameUpdate


class CRUDGame(
    BrokerBase[
        Game,
        GameCreate,
        GameUpdate,
    ]
):
    pass


game = CRUDGame(Game, Game.__tablename__)
