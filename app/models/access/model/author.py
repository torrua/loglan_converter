# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring

from sqlalchemy import Column, Integer, String

from app.models.access.model.base import BaseModel


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
