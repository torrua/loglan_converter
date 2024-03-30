# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring
from sqlalchemy import Column, Integer, String, Text

from app.models.access.model.base import BaseModel


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
