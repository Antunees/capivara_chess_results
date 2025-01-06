from collections.abc import Generator
from typing import Annotated

from fastapi import Depends
from sqlmodel import Session

from app.core.db import engine

def get_db() -> Generator[Session, None, None]:
    with Session(engine) as dbSession:
        yield dbSession


dbSessionDep = Annotated[Session, Depends(get_db)]

