# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring
from app.interfaces.database_interface import DatabaseInterface
from app.models.postgres.connector import PostgresDatabaseConnector
from app.models.storage.storage import Storage


class PostgresInterface(DatabaseInterface):
    def __init__(self, connector: PostgresDatabaseConnector):
        """
        Initialize the PostgresInterface object.
        """
        self.connector = connector

    def export_data(self) -> Storage:
        pass

    def import_data(self, data: Storage):
        pass
