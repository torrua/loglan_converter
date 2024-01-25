# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring
from app.database_interface import DatabaseInterface
from app.storage import Storage
from app.models.access.connector import AccessDatabaseConnector
from logger import logging, logging_time

log = logging.getLogger(__name__)
log.level = logging.INFO


class AccessInterface(DatabaseInterface):
    def __init__(self, connector: AccessDatabaseConnector):
        self.connector = connector

    @logging_time
    def export_data(self) -> Storage:
        s = Storage()
        with self.connector.session() as session:
            for container, class_ in zip(
                s.containers, self.connector.table_order.values()
            ):
                objects = session.query(class_).all()
                log.info("Exporting %s", class_.__name__)
                data = [obj.export_data() for obj in objects]
                container.extend(data)
                log.info("Exported %s %s items\n", len(container), class_.__name__)
        return s

    @logging_time
    def import_data(self, data: Storage):
        pass


if __name__ == "__main__":
    URI = r"C:\Users\User\Dropbox\Python\LOGLA\loglan_convert\data\LoglanDictionary.mdb"
    adc = AccessDatabaseConnector(URI)
    ai = AccessInterface(adc)
    storage = ai.export_data()
    print(storage)
