import logging

from sqlalchemy import Engine
from sqlmodel import Session, select
from tenacity import retry, stop_after_attempt, wait_fixed

import app.crud as crud
from app.core.db import engine

# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)
# stdout_handler = logging.StreamHandler(sys.stdout)
# stdout_handler.setLevel(logging.INFO)

# Cria um formatter e adiciona ao handler
# formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
# stdout_handler.setFormatter(formatter)

# Adiciona o handler ao logger
# logger.addHandler(stdout_handler)

# Teste de log
# logging.info("Este é um log de informação")
# logging.warning("Este é um log de advertência")
# logging.error("Este é um log de erro")

max_tries = 60 * 5  # 5 minutes
wait_seconds = 1


@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    # before=before_log(logger, logging.INFO),
    # after=after_log(logger, logging.WARN),
)
def init(db_engine: Engine) -> None:
    try:
        with Session(db_engine) as session:
            # Try to create session to check if DB is awake
            session.exec(select(1))
    except Exception as e:
        logging.warning(e)
        raise e


def start():
    logging.warning("Initializing service")
    init(engine)
    logging.warning("Service finished initializing")
    print("Service finished initializing")

    tables = ["game", "player"]

    with Session(engine) as dbSession:
        for table in tables:
            objects = getattr(crud.db, table).get_multi(dbSession)
            for item in objects:
                logging.warning(f"Up data from {table} of id {item.id}")
                getattr(crud.broker, table).set(obj_in=item)


if __name__ == "__main__":
    start()
