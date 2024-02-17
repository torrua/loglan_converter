# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring
from app.interface import DatabaseInterface
from app.models.access.connector import AccessDatabaseConnector
from app.models.access.functions import (
    db_clear_content,
    db_compress_file,
    get_unique_values,
)
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

        log.info("Clearing database")
        db_clear_content(self.connector)

        log.info("Compressing database")
        db_compress_file(self.connector)

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


if __name__ == "__main__":
    URI = r"C:\Users\User\Dropbox\Python\LOGLA\loglan_convert\data\LoglanDictionary.mdb"
    adc = AccessDatabaseConnector(URI)
    ai = AccessInterface(adc)
    storage = ai.export_data()

    URI_IMPORT = r"C:\Users\User\Dropbox\Python\LOGLA\
        loglan_convert\data\LoglanDictionaryForImport.mdb"
    adc_import = AccessDatabaseConnector(URI_IMPORT)
    ai_import = AccessInterface(adc_import)
    ai_import.import_data(storage)
