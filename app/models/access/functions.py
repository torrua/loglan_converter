# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring
import os

import win32com.client
from sqlalchemy import MetaData

from app.connector import DatabaseConnector


def db_clear_content(connector: DatabaseConnector):
    """
    Clear content of all tables
    :param connector:
    :return:
    """
    meta = MetaData()
    meta.reflect(bind=connector.engine)

    with connector.session as session:
        for table in reversed(meta.sorted_tables):
            session.execute(table.delete())
        session.commit()


def db_compress_file(connector: DatabaseConnector):
    """
    Compress file
    :param connector:
    :return:
    """
    connector.engine.dispose()

    dst_db = connector.path.replace(".mdb", "_temp.mdb")
    os_app = win32com.client.Dispatch("Access.Application")
    os_app.compactRepair(connector.path, dst_db)
    os_app.Application.Quit()
    os.remove(connector.path)
    os.rename(dst_db, connector.path)


def get_unique_values(objects):
    unique_items = {}
    for item in objects:
        unique_items[str(item)] = item
    return list(unique_items.values())
