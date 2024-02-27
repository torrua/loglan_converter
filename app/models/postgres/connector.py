# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring

import re
from datetime import datetime

from loglan_core import (
    Author,
    Event as BaseEvent,
    Type,
    Word as BaseWord,
    WordSpell,
    Definition,
    Setting as BaseSetting,
    Syllable,
)
from loglan_core.base import BaseModel
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session

from app.connector import DatabaseConnector
from app.models.common import CommonEvent, CommonSetting
from app.properties import ClassName


class Event(BaseEvent):

    def __init__(self, *args, **kwargs):
        date_index = 2
        args = list(args)
        if args and isinstance(args[date_index], str):
            args[date_index] = datetime.strptime(args[date_index], CommonEvent.DATE_FORMAT)
        super().__init__(*args, **kwargs)


class Setting(BaseSetting):

    def __init__(self, *args, **kwargs):
        date_index = 0
        args = list(args)
        if args and isinstance(args[date_index], str):
            args[date_index] = datetime.strptime(args[date_index], CommonSetting.DATE_FORMAT)
        super().__init__(*args, **kwargs)


class PostgresDatabaseConnector(DatabaseConnector):

    def __init__(self, path: str, importing: bool = False):
        if self.is_path(path):
            self.path = path
            self.engine: Engine = self.get_engine(self.path)
            if importing:
                self.recreate_tables()

    @classmethod
    def get_engine(cls, path: str) -> Engine:
        return create_engine(path)

    @property
    def table_order(self):
        return {
            ClassName.authors: Author,
            ClassName.events: Event,
            ClassName.types: Type,
            ClassName.words: BaseWord,
            ClassName.word_spells: WordSpell,
            ClassName.definitions: Definition,
            ClassName.settings: Setting,
            ClassName.syllables: Syllable,
        }

    @property
    def session(self) -> Session:
        return sessionmaker(bind=self.engine, future=True)()

    @staticmethod
    def is_path(path: str) -> bool:
        if not path:
            raise ValueError(
                "No Postgresql URI provided. Please check your environment."
            )

        pattern = r"^postgres(?:ql)?://"
        if re.match(pattern, path) is None:
            raise ValueError(f"Invalid Postgresql URI:\n\t{path}")
        return True

    def recreate_tables(self):
        BaseModel.metadata.drop_all(bind=self.engine)
        BaseModel.metadata.create_all(bind=self.engine)
