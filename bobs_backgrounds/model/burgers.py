from sqlalchemy import Column, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql.elements import Null

from bobs_backgrounds.model.base import BASE


class Burgers(BASE):
    __tablename__ = "burgers"
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False, unique=True)
    explanation = Column(Text, default=Null)
    episode_id = Column(Integer, ForeignKey("episodes.id"), default=Null)
    additional_information = Column(Text, default=Null)

    episode = relationship("Episode", back_populates="burgers")
