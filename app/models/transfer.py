# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring
import os
from app.models.access.connector import AccessDatabaseConnector
from app.models.access.interface import AccessInterface

from app.models.postgres.connector import PostgresDatabaseConnector
from app.models.postgres.interface import PostgresInterface


def ac_to_pg():
    uri = os.environ.get("MDB_DATABASE_URL")
    adc = AccessDatabaseConnector(uri)
    ai = AccessInterface(adc)
    storage = ai.export_data()

    uri_import = os.environ.get("LOD_DATABASE_IMPORT")
    pdc_import = PostgresDatabaseConnector(uri_import)
    pi_import = PostgresInterface(pdc_import)
    pdc_import.recreate_tables()
    pi_import.import_data(storage)


def pg_to_ac():

    uri = os.environ.get("LOD_DATABASE_URL")
    pdc = PostgresDatabaseConnector(uri)
    pi = PostgresInterface(pdc)
    storage = pi.export_data()

    uri_import = os.environ.get("MDB_DATABASE_IMPORT")
    adc = AccessDatabaseConnector(uri_import)
    ai = AccessInterface(adc)
    ai.import_data(storage)


def ac_to_txt():

    uri = os.environ.get("MDB_DATABASE_URL")
    adc = AccessDatabaseConnector(uri)
    ai = AccessInterface(adc)
    storage = ai.export_data()

    uri_import = os.environ.get("TXT_DATABASE_IMPORT")
    adc = AccessDatabaseConnector(uri_import)
    ai = AccessInterface(adc)
    ai.import_data(storage)


if __name__ == "__main__":
    pg_to_ac()
