# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring
from sqlalchemy import Column, Integer, String, Boolean

from app.models.access.model.base import BaseModel


class AccessType(BaseModel):
    """
    Type model
    """

    __tablename__ = "Type"
    sort_name = "Type"

    id = Column(Integer, primary_key=True)
    type_ = Column("type", String(16), nullable=False)
    type_x = Column(String(16), nullable=False)
    group = Column(String(16), nullable=False)
    parentable = Column(Boolean, nullable=False)
    description = Column(String(255), nullable=True)

    def export_data(self):
        return [
            self.type_,
            self.type_x,
            self.group,
            self.parentable,
            self.ves(self.description),
        ]

    @classmethod
    def import_data(cls, item: list[str]):
        return {
            "type_": item[0],
            "type_x": item[1],
            "group": cls.von(item[2]),
            "parentable": item[3],
            "description": cls.von(item[4]),
        }
