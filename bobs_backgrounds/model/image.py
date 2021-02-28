from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql.elements import Null

from model import BASE

if TYPE_CHECKING:
    from model.burger import Burger


class Image(BASE):
    __tablename__ = "images"

    id: int = Column(Integer, primary_key=True)
    path: str = Column(Text, nullable=False)
    created_at: datetime = Column(DateTime, nullable=False)
    archived_at: datetime = Column(DateTime, default=Null)
    burger_id: int = Column(Integer, ForeignKey("burgers.id"))

    burger: "Burger" = relationship("Burger", back_populates="images")
