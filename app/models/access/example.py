# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring

import os
from pprint import pprint

from sqlalchemy import select

from app.models.access.connector import AccessDatabaseConnector
from app.models.access.model import AccessWordSpell as WordSpell

if __name__ == "__main__":
    MDB_URI = os.environ.get("MDB_DATABASE_URL")
    acd = AccessDatabaseConnector(MDB_URI)
    session = acd.session()

    words = session.execute(select(WordSpell).where(WordSpell.word.like("pro%"))).scalars().all()
    pprint(words)
    print(len(words))
