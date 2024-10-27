# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring
from sqlalchemy import Column, Integer, String, Text

from app.models.access.model.base import BaseModel


class AccessWord(BaseModel):
    """
    Word model
    """

    __tablename__ = "Words"
    sort_name = "Word"

    word_id = Column("WID", Integer, nullable=False, primary_key=True)
    type_ = Column("Type", String(16), nullable=False)
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
            self.type_,
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
            "type_": item[1],
            "type_x": item[2],
            "affixes": cls.von(item[3]),
            "match": cls.von(item[4]),
            "authors": cls.von(item[5]),
            "year": cls.von(item[6]),
            "rank": cls.von(item[7]),
            "origin": cls.von(item[8]),
            "origin_x": cls.von(item[9]),
            "used_in": cls.von(item[10]),
            "TID_old": cls.von(item[11]),
        }
