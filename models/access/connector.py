# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring

from urllib.parse import quote_plus

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker


class AccessDatabaseConnector:
    DRIVER = (
        r"DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={};ExtendedAnsiSQL=1;"
    )

    def __init__(self, db_path: str):
        self.engine = self.create_engine(db_path)

    @classmethod
    def create_engine(cls, db_path: str) -> Engine:
        connection_string = cls.DRIVER.format(db_path)
        connection_url = (
            f"access+pyodbc:///?odbc_connect={quote_plus(connection_string)}"
        )
        return create_engine(connection_url)

    def session(self) -> Session:
        return sessionmaker(bind=self.engine)()
