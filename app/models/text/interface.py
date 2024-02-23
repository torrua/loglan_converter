# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring
import datetime
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
                split_lines = [
                    line.strip().split(self.SEPARATOR) for line in f.readlines()
                ]
                s.container_by_name(class_name).extend(split_lines)
        return s

    def import_data(self, data: Storage):
        date_marker = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        full_path = os.path.join(self.connector.path, date_marker)
        if not os.path.exists(full_path):
            os.makedirs(full_path)

        for container_name in data.names:
            file_content = self.generate_file_content(container_name, data, self.SEPARATOR)
            file_name = f"{date_marker}_{container_name}.{self.connector.EXTENSION}"
            file_path = os.path.join(full_path, file_name)
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(file_content)

    @staticmethod
    def generate_file_content(container_name, data, separator):
        lines = []
        for item in data.container_by_name(container_name):
            item = [str(i) if i is not None else "" for i in item]
            lines.append(separator.join(item))
        return "\n".join(lines)


if __name__ == "__main__":
    uri = os.environ.get("TXT_DATABASE_URL")
    tc = TextConnector(uri)

    for name in ClassName():
        print(tc.path_by_name(name))

    ti = TextInterface(tc)

    storage_with_exported_data = ti.export_data()

    print(storage_with_exported_data)

    uri_i = os.environ.get("TXT_DATABASE_IMPORT")
    tc_i = TextConnector(uri_i, importing=True)
    tii = TextInterface(tc_i)

    tii.import_data(storage_with_exported_data)
