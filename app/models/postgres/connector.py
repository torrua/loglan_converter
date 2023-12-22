# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring

import re

from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session


class PostgresDatabaseConnector:
    def __init__(self, path: str):
        if self.is_path(path):
            self.engine = self.get_engine(path)

    @classmethod
    def get_engine(cls, path: str) -> Engine:
        return create_engine(path)

    def session(self) -> Session:
        return sessionmaker(bind=self.engine, future=True)()

    @staticmethod
    def is_path(path: str) -> bool:
        if not path:
            raise ValueError("No Postgresql URI provided. Please check your environment.")

        pattern = r"^postgres(?:ql)?://"
        if re.match(pattern, path) is None:
            raise ValueError(f"Invalid Postgresql URI:\n\t{path}")
        return True
