# pylint: disable=missing-module-docstring
from abc import ABC, abstractmethod

from app.models.storage.storage import Storage


class DatabaseInterface(ABC):
    """
    An abstract class representing a database interface.
    """

    SEPARATOR = "@"

    @abstractmethod
    def export_data(self) -> Storage:
        """
        Exports data from the database to a Storage object.

        Returns:
            Storage: A Storage object containing the exported data.
        """

    @abstractmethod
    def import_data(self, data: Storage):
        """
        Imports a Storage object to the database.

        Parameters:
            data (Storage): The Storage object to import.
        """
