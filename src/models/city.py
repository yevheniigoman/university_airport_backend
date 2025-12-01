from db import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class City(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)

    # City.airports to get list of airports in this city
    airports = relationship("Airport", back_populates="city")