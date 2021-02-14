from sqlalchemy import Column, Integer, Text, UniqueConstraint

from bobs_backgrounds.model.base import BASE


class Episodes(BASE):
    __tablename__ = "episodes"
    __table_args__ = UniqueConstraint("season", "number", "episodes_season_number_uindex")
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    season = Column(Integer)
    number = Column(Integer)
