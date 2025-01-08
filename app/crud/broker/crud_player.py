import hashlib
import logging
from app.crud.broker.base import BrokerBase
from app.models.player import Player, PlayerCreate, PlayerUpdate

class CRUDPlayer(
    BrokerBase[
        Player,
        PlayerCreate,
        PlayerUpdate,
    ]
):
    def set(self, *, obj_in: Player) -> None:
        super().set(obj_in=obj_in)
        key = f"{self.tablename}:by_name:{obj_in.name}"
        super().set_specific_key(key=key, obj_in=obj_in)

        md5_hash = f'{obj_in.id}:{obj_in.secret}'.encode('utf-8')
        md5_hash = hashlib.md5(md5_hash).hexdigest()
        key = f"player_id_secret:{md5_hash}"
        super().set_string_on_specific_key(key=key, text=md5_hash)

    def get_by_name(self, *, name: str) -> Player:
        return super().get_specific_key(f"{self.tablename}:by_name:{name}")

    def is_active(self, player: Player) -> bool:
        return player.is_active


player = CRUDPlayer(Player, Player.__tablename__)
