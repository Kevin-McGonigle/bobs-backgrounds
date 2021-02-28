from typing import List, TYPE_CHECKING

from sqlalchemy import Column, Integer, Text, UniqueConstraint
from sqlalchemy.orm import relationship

from model import BASE

if TYPE_CHECKING:
    from model.burger import Burger


class Episode(BASE):
    __tablename__ = "episodes"
    __table_args__ = UniqueConstraint("season", "number", "episodes_season_number_uindex")

    id: int = Column(Integer, primary_key=True)
    name: str = Column(Text, nullable=False)
    season: int = Column(Integer)
    number: int = Column(Integer)

    burgers: List[Burger] = relationship("Burger", back_populates="episode")
