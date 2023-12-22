# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring

import re

from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session


class PostgresDatabaseConnector:
    def __init__(self, uri: str):
        if self.is_uri(uri):
            self.engine = self.get_engine(uri)

    @classmethod
    def get_engine(cls, uri: str) -> Engine:
        return create_engine(uri)

    def session(self) -> Session:
        return sessionmaker(bind=self.engine, future=True)()

    @staticmethod
    def is_uri(uri) -> bool:
        if not uri:
            raise ValueError("No Postgresql URI provided. Please check your environment.")

        pattern = r"^postgres(?:ql)?://"
        if re.match(pattern, uri) is None:
            raise ValueError(f"Invalid Postgresql URI:\n\t{uri}")
        return True
