# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring
import os

from app.interface import DatabaseInterface
from app.models.text.connector import TextConnector
from app.properties import ClassName
from app.storage import Storage


class TextInterface(DatabaseInterface):
    def __init__(self, connector: TextConnector):
        self.connector = connector

    def export_data(self) -> Storage:
        """
        Export data from the TextConnector object.
        :return:
        """
        s = Storage()
        for class_name in ClassName():
            path = self.connector.path_by_name(class_name)
            with open(path, "r", encoding="utf-8") as f:
                split_lines = [line.strip().split(self.SEPARATOR) for line in f.readlines()]
                s.container_by_name(class_name).extend(split_lines)

        return s

    def import_data(self, data: Storage):
        pass


if __name__ == "__main__":
    uri = os.environ.get("TXT_DATABASE_URL")
    tc = TextConnector(uri)

    for name in ClassName():
        print(tc.path_by_name(name))

    ti = TextInterface(tc)
    print(ti)

    export = ti.export_data()

    print(export)
