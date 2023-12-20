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
        return f"{self.abbreviation}@{self.full_name}@{self.notes or ''}"

    @staticmethod
    def import_data(item: list[str]):
        return {
            "abbreviation": item[0],
            "full_name": item[1] or None,
            "notes": item[2] or None,
        }


class AccessDefinition(BaseModel):
    __tablename__ = "WordDefinition"
    sort_name = "Definition"

    word_id = Column("WID", Integer)
    position = Column("I", Integer, nullable=False)
    usage = Column("Usage", String(64))
    grammar = Column("Grammar", String(8))
    body = Column("Definition", Text, nullable=False)
    main = Column("Main", String(8))
    case_tags = Column("Tags", String(16))
    id = Column("id", Integer, primary_key=True)

    def export_data(self):
        return (
            f"{self.word_id}@{self.position}@{self.usage or ''}"
            f"@{self.grammar or ''}@{self.body}@@{self.case_tags or ''}"
        )

    @staticmethod
    def import_data(item: list[str]):
        return {
            "word_id": int(item[0]),
            "position": int(item[1]),
            "usage": item[2] or None,
            "grammar": item[3] or None,
            "body": item[4],
            "main": item[5] or None,
            "case_tags": item[6] or None,
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
        return (
            f"{self.id}@{self.name}"
            f"@{self.date}@{self.definition}"
            f"@{self.annotation or ''}"
            f"@{self.suffix or ''}"
        )

    @staticmethod
    def import_data(item: list[str]):
        return {
            "id": int(item[0]),
            "name": item[1],
            "date": item[2],
            "definition": item[3],
            "annotation": item[4] or None,
            "suffix": item[5] or None,
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
        return (
            f"{self.date.strftime('%d.%m.%Y %H:%M:%S')}"
            f"@{self.db_version}@{self.last_word_id}@{self.db_release}"
        )

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
        return f"{self.name}@{self.type}@{self.allowed}"

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
        return (
            f"{self.type}@{self.type_x}@{self.group}@{self.parentable}"
            f"@{self.description or ''}"
        )

    @staticmethod
    def import_data(item: list[str]):
        return {
            "type": item[0],
            "type_x": item[1],
            "group": item[2] or None,
            "parentable": ast.literal_eval(item[3]),
            "description": item[4] or "",
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

        return (
            f"{self.word_id}@{self.type}@{self.type_x}"
            f"@{self.affixes or ''}"
            f"@{self.match or ''}"
            f"@{self.authors}"
            f"@{self.year}"
            f"@{self.rank or ''}"
            f"@{self.origin or ''}"
            f"@{self.origin_x or ''}"
            f"@{self.used_in or ''}"
            f"@{self.TID_old or ''}"
        )

    @staticmethod
    def import_data(item: list[str]):
        return {
            "word_id": int(item[0]),
            "type": item[1],
            "type_x": item[2],
            "affixes": item[3] or None,
            "match": item[4] or None,
            "authors": item[5] or None,
            "year": item[6] or None,
            "rank": item[7] or None,
            "origin": item[8] or None,
            "origin_x": item[9] or None,
            "used_in": item[10] or None,
            "TID_old": int(item[11]) or None,
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
        return (
            f"{self.word_id}@{self.word}@{self.word.lower()}@{code_name}"
            f"@{self.event_start_id}@{self.event_end_id}@{self.origin_x or ''}"
        )

    @staticmethod
    def import_data(item: list[str]):
        return {
            "word_id": int(item[0]),
            "word": item[1],
            "sort_a": item[2],
            "sort_b": item[3],
            "event_start_id": int(item[4]),
            "event_end_id": int(item[5]),
            "origin_x": item[6] or None,
        }
