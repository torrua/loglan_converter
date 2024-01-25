# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring

import ast
from datetime import datetime

from sqlalchemy import Column, String, Integer, Text, Boolean, DateTime
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
        super().__init__(**kwargs)
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


class AccessAuthor(BaseModel):
    """
    Author model
    """

    __tablename__ = "Author"
    sort_name = "Author"

    id = Column(Integer, primary_key=True)
    abbreviation = Column(String(64), unique=True, nullable=False)
    full_name = Column(String(64))
    notes = Column(String(128))

    def export_data(self):
        return [
            self.abbreviation,
            self.full_name,
            self.ves(self.notes),
        ]

    @classmethod
    def import_data(cls, item: list[str]):
        return {
            "abbreviation": item[0],
            "full_name": cls.von(item[1]),
            "notes": cls.von(item[2]),
        }


class AccessDefinition(BaseModel):
    __tablename__ = "WordDefinition"
    sort_name = "Definition"

    word_id = Column("WID", Integer, nullable=False)
    position = Column("I", Integer, nullable=False)
    usage = Column("Usage", String(64))
    grammar = Column("Grammar", String(8))
    body = Column("Definition", Text, nullable=False)
    main = Column("Main", String(8))
    case_tags = Column("Tags", String(16))
    id = Column("id", Integer, primary_key=True)

    def export_data(self):
        return [
            self.word_id,
            self.position,
            self.ves(self.usage),
            self.ves(self.grammar),
            self.body,
            self.ves(self.main),
            self.ves(self.case_tags),
        ]

    @classmethod
    def import_data(cls, item: list[str]):
        return {
            "word_id": int(item[0]),
            "position": int(item[1]),
            "usage": cls.von(item[2]),
            "grammar": cls.von(item[3]),
            "body": item[4],
            "main": cls.von(item[5]),
            "case_tags": cls.von(item[6]),
        }


class AccessEvent(BaseModel):
    """
    Event model
    """

    __tablename__ = "LexEvent"
    sort_name = "Event"

    id = Column("EVT", Integer, primary_key=True)
    name = Column("Event", String(64), nullable=False)
    date = Column("When", String(32), nullable=False)
    definition = Column("WhyWhat", Text, nullable=False)
    annotation = Column("DictionaryAnnotation", String(16))
    suffix = Column("FilenameSuffix", String(16))

    def export_data(self):
        return [
            self.id,
            self.name,
            self.date,
            self.definition,
            self.ves(self.annotation),
            self.ves(self.suffix),
        ]

    @classmethod
    def import_data(cls, item: list[str]):
        return {
            "id": int(item[0]),
            "name": item[1],
            "date": item[2],
            "definition": item[3],
            "annotation": cls.von(item[4]),
            "suffix": cls.von(item[5]),
        }


class AccessSetting(BaseModel):
    """
    Setting model
    """

    __tablename__ = "Settings"
    sort_name = "Settings"

    date = Column("DateModified", DateTime, primary_key=True)
    db_version = Column("DBVersion", Integer, nullable=False)
    last_word_id = Column("LastWID", Integer, nullable=False)
    db_release = Column("DBRelease", String(16), nullable=False)

    def export_data(self):
        return [
            self.date.strftime("%d.%m.%Y %H:%M:%S"),
            self.db_version,
            self.last_word_id,
            self.db_release,
        ]

    @staticmethod
    def import_data(item: list[str]):
        return {
            "date": datetime.strptime(item[0], "%d.%m.%Y %H:%M:%S"),
            "db_version": int(item[1]),
            "last_word_id": int(item[2]),
            "db_release": item[3],
        }


class AccessSyllable(BaseModel):
    """
    Syllable model
    """

    __tablename__ = "Syllable"
    sort_name = "Syllable"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column("characters", String(8), primary_key=True)
    type = Column(String(32), nullable=False)
    allowed = Column(Boolean)

    def export_data(self):
        return [
            self.name,
            self.type,
            self.allowed,
        ]

    @staticmethod
    def import_data(item: list[str]):
        return {
            "name": item[0],
            "type": item[1],
            "allowed": ast.literal_eval(item[2]) if item[2] else False,
        }


class AccessType(BaseModel):
    """
    Type model
    """

    __tablename__ = "Type"
    sort_name = "Type"

    id = Column(Integer, primary_key=True)
    type = Column(String(16), nullable=False)
    type_x = Column(String(16), nullable=False)
    group = Column(String(16), nullable=False)
    parentable = Column(Boolean, nullable=False)
    description = Column(String(255), nullable=True)

    def export_data(self):
        return [
            self.type,
            self.type_x,
            self.group,
            self.parentable,
            self.ves(self.description),
        ]

    @classmethod
    def import_data(cls, item: list[str]):
        return {
            "type": item[0],
            "type_x": item[1],
            "group": cls.von(item[2]),
            "parentable": ast.literal_eval(item[3]),
            "description": cls.von(item[4]),
        }


class AccessWord(BaseModel):
    """
    Word model
    """

    __tablename__ = "Words"
    sort_name = "Word"

    word_id = Column("WID", Integer, nullable=False, primary_key=True)
    type = Column("Type", String(16), nullable=False)
    type_x = Column("XType", String(16), nullable=False)
    affixes = Column("Affixes", String(16))
    match = Column("Match", String(8))
    authors = Column("Source", String(64))
    year = Column("Year", String(128))
    rank = Column("Rank", String(128))
    origin = Column("Origin", String(128))
    origin_x = Column("OriginX", String(64))
    used_in = Column("UsedIn", Text)
    TID_old = Column("TID", Integer)  # references

    def export_data(self):
        """
        Prepare Word data for exporting to text file
        :return: Formatted basic string
        """
        return [
            self.word_id,
            self.type,
            self.type_x,
            self.ves(self.affixes),
            self.ves(self.match),
            self.authors,
            self.year,
            self.ves(self.rank),
            self.ves(self.origin),
            self.ves(self.origin_x),
            self.ves(self.used_in),
            self.TID_old,
        ]

    @classmethod
    def import_data(cls, item: list[str]):
        return {
            "word_id": int(item[0]),
            "type": item[1],
            "type_x": item[2],
            "affixes": cls.von(item[3]),
            "match": cls.von(item[4]),
            "authors": cls.von(item[5]),
            "year": cls.von(item[6]),
            "rank": cls.von(item[7]),
            "origin": cls.von(item[8]),
            "origin_x": cls.von(item[9]),
            "used_in": cls.von(item[10]),
            "TID_old": cls.von(int(item[11])),
        }


class AccessWordSpell(BaseModel):
    """WordSpell model"""

    __tablename__ = "WordSpell"
    sort_name = "WordSpell"

    word_id = Column("WID", Integer, nullable=False)
    word = Column("Word", String(64), nullable=False)
    sort_a = Column("SortA", String(64), nullable=False)
    sort_b = Column("SortB", String(64), nullable=False)
    event_start_id = Column("SEVT", Integer, nullable=False)
    event_end_id = Column("EEVT", Integer, nullable=False)
    origin_x = Column("OriginX", String(64))
    id = Column(Integer, primary_key=True)

    def export_data(self):
        """
        Prepare Word Spell data for exporting to text file
        :return: Formatted basic string
        """
        code_name = "".join(["0" if symbol.isupper() else "5" for symbol in self.word])
        return [
            self.word_id,
            self.word,
            self.word.lower(),
            code_name,
            self.event_start_id,
            self.event_end_id,
            self.ves(self.origin_x),
        ]

    @classmethod
    def import_data(cls, item: list[str]):
        return {
            "word_id": int(item[0]),
            "word": item[1],
            "sort_a": item[2],
            "sort_b": item[3],
            "event_start_id": int(item[4]),
            "event_end_id": int(item[5]),
            "origin_x": cls.von(item[6]),
        }
