# pylint: disable=missing-module-docstring
from abc import ABC, abstractmethod

from app.connector import DatabaseConnector
from app.storage import Storage
from logger import logging

log = logging.getLogger(__name__)
log.level = logging.ERROR


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

    @staticmethod
    def default_export(connector: DatabaseConnector, data_getter):
        """Default way to export data from the database to a Storage object."""
        s = Storage()
        with connector.session as session:
            for container, class_ in zip(s.containers, connector.table_order.values()):
                objects = session.query(class_).all()
                log.info("Exporting %s", class_.__name__)

                data = data_getter(objects)
                container.extend(data)

                log.info("Exported %s %s items\n", len(container), class_.__name__)
        return s

    def __repr__(self):
        return f"{self.__class__.__name__}({self.__dict__})"
