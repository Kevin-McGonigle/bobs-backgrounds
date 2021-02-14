from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql.elements import Null

from bobs_backgrounds.model.base import BASE


class Images(BASE):
    __tablename__ = "images"
    id = Column(Integer, primary_key=True)
    path = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False)
    archived_at = Column(DateTime, default=Null)
    burger_id = Column(Integer, ForeignKey("burgers.id"))

    burger = relationship("Burger", back_populates="images")
