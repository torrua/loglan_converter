# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring
from sqlalchemy import Column, Integer, String

from app.models.access.model.base import BaseModel


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
