# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring

import os

from sqlalchemy import select

from app.models.access.connector import AccessDatabaseConnector
from app.models.access.model import AccessWordSpell as WordSpell, AccessWord as Word

if __name__ == "__main__":
    MDB_URI = os.environ.get("MDB_DATABASE_URL")
    acd = AccessDatabaseConnector(MDB_URI)
    session = acd.session()

    word_spells = (
        session.execute(select(WordSpell).where(WordSpell.word_id == 7180))
        .scalars()
        .all()
    )
    words = session.execute(select(Word).where(Word.word_id == 7180)).scalars().all()
    for w in words:
        print(w.export_data())

    print(len(words))
