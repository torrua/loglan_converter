# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring

import re
from urllib.parse import quote_plus

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker


class AccessDatabaseConnector:
    DRIVER = (
        r"DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={};ExtendedAnsiSQL=1;"
    )

    def __init__(self, path: str):
        if self.is_path(path):
            self.engine = self.get_engine(path)

    @classmethod
    def get_engine(cls, path: str) -> Engine:
        connection_string = cls.DRIVER.format(path)
        connection_url = (
            f"access+pyodbc:///?odbc_connect={quote_plus(connection_string)}"
        )
        return create_engine(connection_url)

    def session(self) -> Session:
        return sessionmaker(bind=self.engine)()

    @staticmethod
    def is_path(path: str) -> bool:
        if not path:
            raise ValueError(
                "No Microsoft Access URI provided. Please check your environment."
            )

        pattern = r"^.*\.mdb|accdb$"
        if re.match(pattern, path) is None:
            raise ValueError(f"Invalid Microsoft Access URI:\n\t{path}")
        return True