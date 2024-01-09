# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring
from app.interfaces.database_interface import DatabaseInterface
from app.models.storage.storage import Storage


class TextInterface(DatabaseInterface):
    def __init__(self, connector):
        pass

    def export_data(self) -> Storage:
        pass

    def import_data(self, data: Storage):
        pass
