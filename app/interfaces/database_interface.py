# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring
from abc import ABC, abstractmethod
from app.models.storage.storage import Storage


class DatabaseInterface(ABC):

    @abstractmethod
    def export_data(self) -> Storage:
        ...

    @abstractmethod
    def import_data(self, data: Storage):
        ...
