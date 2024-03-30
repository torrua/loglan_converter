# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring
from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String

from app.models.access.model.base import BaseModel
from app.models.common import CommonSetting


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
            self.date.strftime(CommonSetting.DATE_FORMAT),
            self.db_version,
            self.last_word_id,
            self.db_release,
        ]

    @staticmethod
    def import_data(item: list[str]):
        return {
            "date": datetime.strptime(item[0], CommonSetting.DATE_FORMAT),
            "db_version": int(item[1]),
            "last_word_id": int(item[2]),
            "db_release": item[3],
        }
