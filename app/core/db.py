import logging
import uuid
from sqlmodel import Session, create_engine, select
from app.models import Player, PlayerCreate
from app import crud

from app.core.config import settings

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))


# make sure all SQLModel models are imported (app.models) before initializing DB
# otherwise, SQLModel might fail to initialize relationships properly
# for more details: https://github.com/fastapi/full-stack-fastapi-template/issues/28


def init_db(session: Session) -> None:
    draw_player = session.exec(
        select(Player).where(Player.name == 'DRAW')
    ).first()
    if not draw_player:
        player_in = Player(
            name="DRAW",
            id="00000000-0000-0000-0000-000000000000",
            is_active=True
        )
        draw_player = crud.db.player.create(dbSession=session, obj_in=player_in)
