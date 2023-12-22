# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring

import os
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker


class TextConnector:

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
        if os.path.exists(path):
            return True
        raise FileNotFoundError("Directory not found")
