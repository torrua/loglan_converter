# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring
from sqlalchemy.orm import DeclarativeBase


class BaseModel(DeclarativeBase):
    """
    Base class for common methods
    """

    __abstract__ = True

    def __repr__(self):
        """
        Special method that returns a string representation of the object.
        It forms the string by joining key-value pairs of the object's attributes,
        excluding keys that start with "_" and keys that are "created" or "updated".
        The key-value pairs are sorted before joining.

        Returns:
            str: A string representation of the object in the format:
                 "ClassName(key1=value1, key2=value2, ...)".
        """
        obj_str = ", ".join(
            sorted(
                [
                    f"{k}={v!r}"
                    for k, v in self.__dict__.items()
                    if not k.startswith("_") and k not in ["created", "updated"] and v
                ]
            )
        )
        return f"{self.__class__.__name__}({obj_str})"

    def __init__(self, *initial_data, **kwargs):
        """Constructor"""
        super().__init__()
        for dictionary in initial_data:
            for key in dictionary:
                setattr(self, key, dictionary[key])
        for key, value in kwargs.items():
            setattr(self, key, value)

    def export_data(self):
        pass

    @staticmethod
    def value_or_none(value):
        return value if value else None

    von = value_or_none

    @staticmethod
    def value_or_empty_string(value):
        return value if value else ""

    ves = value_or_empty_string
