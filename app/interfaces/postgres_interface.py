# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring
from app.interfaces.database_interface import DatabaseInterface
from app.models.storage.storage import Storage


class PostgresInterface(DatabaseInterface):

    def export_data(self) -> Storage:
        pass

    def import_data(self, data: Storage):
        pass
