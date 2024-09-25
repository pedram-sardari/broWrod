from typing import Generator

from db.session import Client


def get_db_cli() -> Generator:  # todo: can this be a coroutine?
    db_cli = Client()
    try:
        yield db_cli
    finally:
        db_cli.close()
        print('%'*20, 'closing the db client', '%'*20)
