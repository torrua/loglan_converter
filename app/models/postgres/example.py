# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring

import os
from pprint import pprint
from loglan_core.addons.word_selector import WordSelector
from app.models.postgres.connector import PostgresDatabaseConnector


if __name__ == "__main__":
    LOD_URI = os.environ.get("LOD_DATABASE_URL")
    pdc = PostgresDatabaseConnector(LOD_URI)
    session = pdc.session()

    words = WordSelector().by_name("pro*").all(session)
    pprint(words)
    print(len(words))
