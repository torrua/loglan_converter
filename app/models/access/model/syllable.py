# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring
from sqlalchemy import Column, Integer, String, Boolean

from app.models.access.model.base import BaseModel


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
            "allowed": item[2] or False,
        }
