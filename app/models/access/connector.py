# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring

import re
from urllib.parse import quote_plus

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.connector import DatabaseConnector
from app.models.access.functions import db_compress_file, db_clear_content
from app.models.access.model import (
    AccessAuthor,
    AccessEvent,
    AccessSetting,
    AccessSyllable,
    AccessType,
    AccessWord,
    AccessWordSpell,
    AccessDefinition,
)
from app.properties import ClassName
from logger import log


class AccessDatabaseConnector(DatabaseConnector):
    DRIVER = (
        r"DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={};ExtendedAnsiSQL=1;"
    )

    def __init__(self, path: str, importing: bool = False):
        self.is_path(path)
        self.path = path
        self.engine = self.get_engine(self.path)

        if importing:
            log.info("Clearing database")
            db_clear_content(self)

            log.info("Compressing database")
            db_compress_file(self)

    @classmethod
    def get_engine(cls, path: str) -> Engine:
        connection_string = cls.DRIVER.format(path)
        connection_url = (
            f"access+pyodbc:///?odbc_connect={quote_plus(connection_string)}"
        )
        return create_engine(connection_url)

    @property
    def table_order(self):
        return {
            ClassName.authors: AccessAuthor,
            ClassName.events: AccessEvent,
            ClassName.types: AccessType,
            ClassName.words: AccessWord,
            ClassName.word_spells: AccessWordSpell,
            ClassName.definitions: AccessDefinition,
            ClassName.settings: AccessSetting,
            ClassName.syllables: AccessSyllable,
        }

    @property
    def session(self) -> Session:
        return sessionmaker(bind=self.engine)()

    @staticmethod
    def is_path(path: str):
        if not path:
            raise ValueError(
                "No Microsoft Access URI provided. Please check your environment."
            )

        pattern = r"^.*\.mdb|accdb$"
        if re.match(pattern, path) is None:
            raise ValueError(f"Invalid Microsoft Access URI:\n\t{path}")
