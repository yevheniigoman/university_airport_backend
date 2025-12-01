from db import Base
from sqlalchemy import Column, Integer, String, DECIMAL
from sqlalchemy.orm import relationship


class Aircraft(Base):
    __tablename__ = "aircrafts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    tail_number = Column(String(10), unique=True, nullable=False)
    model = Column(String(50), nullable=False)
    fuel_per_hour = Column(DECIMAL(10, 2), nullable=False)
    total_seats = Column(Integer, nullable=False)

    seats = relationship("Seat", back_populates="aircraft")
