# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring
from abc import ABC, abstractmethod

from sqlalchemy import Engine
from sqlalchemy.orm import Session


class DatabaseConnector(ABC):
    """Database connector"""

    path: str
    engine: Engine

    @property
    @abstractmethod
    def table_order(self) -> dict:
        pass

    @property
    @abstractmethod
    def session(self) -> Session:
        pass
