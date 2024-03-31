# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring
from app.models.access.connector import AccessDatabaseConnector
from app.models.access.interface import AccessInterface

from app.models.postgres.connector import PostgresDatabaseConnector
from app.models.postgres.interface import PostgresInterface

from app.models.text.connector import TextConnector
from app.models.text.interface import TextInterface


def storage_from(path, connector, interface):
    connector = connector(path)
    interface = interface(connector)
    return interface.export_data()


def storage_to(path, storage, connector, interface):
    connector = connector(path, importing=True)
    interface = interface(connector)
    interface.import_data(storage)


def storage_from_ac(path):
    return storage_from(path, AccessDatabaseConnector, AccessInterface)


def storage_from_pg(path):
    return storage_from(path, PostgresDatabaseConnector, PostgresInterface)


def storage_from_txt(path):
    return storage_from(path, TextConnector, TextInterface)


def storage_to_ac(path, storage):
    return storage_to(path, storage, AccessDatabaseConnector, AccessInterface)


def storage_to_pg(path, storage):
    return storage_to(path, storage, PostgresDatabaseConnector, PostgresInterface)


def storage_to_txt(path, storage):
    return storage_to(path, storage, TextConnector, TextInterface)


if __name__ == "__main__":
    pass
