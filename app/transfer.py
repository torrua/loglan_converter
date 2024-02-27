# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring
from app.models.access.connector import AccessDatabaseConnector
from app.models.access.interface import AccessInterface

from app.models.postgres.connector import PostgresDatabaseConnector
from app.models.postgres.interface import PostgresInterface

from app.models.text.connector import TextConnector
from app.models.text.interface import TextInterface


def storage_from_ac(path):
    adc = AccessDatabaseConnector(path)
    ai = AccessInterface(adc)
    return ai.export_data()


def storage_from_pg(path):
    pdc = PostgresDatabaseConnector(path)
    pi = PostgresInterface(pdc)
    return pi.export_data()


def storage_from_txt(path):
    tc = TextConnector(path)
    ti = TextInterface(tc)
    return ti.export_data()


def storage_to_ac(path, storage):
    adc = AccessDatabaseConnector(path, importing=True)
    ai = AccessInterface(adc)
    ai.import_data(storage)


def storage_to_pg(path, storage):
    pdc = PostgresDatabaseConnector(path, importing=True)
    pi = PostgresInterface(pdc)
    pi.import_data(storage)


def storage_to_txt(path, storage):
    tc = TextConnector(path, importing=True)
    ti = TextInterface(tc)
    ti.import_data(storage)


if __name__ == "__main__":
    pass
