# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring

import os
from loglan_core.addons.word_selector import WordSelector
from app.models.postgres.connector import PostgresDatabaseConnector
from loglan_core.addons.exporter import Exporter

if __name__ == "__main__":
    LOD_URI = os.environ.get("LOD_DATABASE_URL")
    pdc = PostgresDatabaseConnector(LOD_URI)
    session = pdc.session()

    words = WordSelector().filter_by(id_old=7180).all(session)
    for w in words:
        print(Exporter.export(w))
