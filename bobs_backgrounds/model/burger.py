from typing import List

from sqlalchemy import Column, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql.elements import Null

from model import BASE
from model.episode import Episode
from model.image import Image


class Burger(BASE):
    __tablename__ = "burgers"

    id: int = Column(Integer, primary_key=True)
    name: str = Column(Text, nullable=False, unique=True)
    explanation: str = Column(Text, default=Null)
    episode_id: str = Column(Integer, ForeignKey("episodes.id"), default=Null)
    additional_information: str = Column(Text, default=Null)

    episode: Episode = relationship("Episode", back_populates="burgers")
    images: List[Image] = relationship("Image", back_populates="burger")
