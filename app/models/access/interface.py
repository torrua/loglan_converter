# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring
from app.interface import DatabaseInterface
from app.models.access.connector import AccessDatabaseConnector
from app.models.access.functions import get_unique_values
from app.storage import Storage
from logger import logging, logging_time

log = logging.getLogger(__name__)
log.level = logging.INFO


class AccessInterface(DatabaseInterface):
    def __init__(self, connector: AccessDatabaseConnector):
        self.connector = connector

    @logging_time
    def export_data(self) -> Storage:
        return self.default_export(self.connector, self.get_data_from_objects)

    @staticmethod
    def get_data_from_objects(objects):
        return [obj.export_data() for obj in objects]

    @logging_time
    def import_data(self, data: Storage):

        log.info("Start to fill tables with dictionary data")
        model_names = self.connector.table_order.keys()

        with self.connector.session as session:

            for model_name in model_names:
                container = data.container_by_name(model_name)
                model = self.connector.table_order.get(model_name)
                log.info("Start to process %s objects", model.__name__)
                objects = [model(**model.import_data(item)) for item in container]
                log.info(
                    "Total number of %s objects - %s", model.__name__, len(objects)
                )
                objects = get_unique_values(objects)
                log.info(
                    "Total number of unique %s objects - %s",
                    model.__name__,
                    len(objects),
                )
                log.info("Add %s objects to Database", model.__name__)
                session.bulk_save_objects(objects)
                log.debug("Commit Database changes")
                session.commit()
                log.info("Finish to process %s objects\n", model.__name__)
        log.info("Finish to fill tables with dictionary data\n")
