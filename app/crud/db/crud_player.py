from typing import Optional
import uuid

from sqlalchemy.orm import Session

import app.crud.broker.crud_player as crud_player
from app import crud
from fastapi.encoders import jsonable_encoder
from app.crud.db.base import CRUDBase
from app.models.player import Player, PlayerCreate, PlayerUpdate


class CRUDPlayer(CRUDBase[Player, PlayerCreate, PlayerUpdate, crud_player.CRUDPlayer]):
    def get_by_name(self, dbSession: Session, *, name: str) -> Optional[Player]:
        return dbSession.query(Player).filter(Player.name == name).first()

    def is_active(self, player: Player) -> bool:
        return player.is_active

    def create(self, dbSession: Session, *, obj_in: PlayerCreate) -> Player:
        obj_in.secret = uuid.uuid4()
        return super().create(dbSession=dbSession, obj_in=obj_in)

player = CRUDPlayer(Player, crud_player.CRUDPlayer)
