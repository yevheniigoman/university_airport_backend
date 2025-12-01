from db import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class Airport(Base):
    __tablename__ = "airports"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    # the code consists of 3 letters: LAX, JFX, PRG
    code = Column(String(3), nullable=False, unique=True)
    city_id = Column(Integer, ForeignKey("cities.id"), nullable=False)

    # Airport.city to know where airport is located
    city = relationship("City", back_populates="airports")
