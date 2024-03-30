# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring
from sqlalchemy import Column, Integer, String, Text

from app.models.access.model.base import BaseModel


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
