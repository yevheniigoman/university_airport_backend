from db import Base
from sqlalchemy import Column, Integer, String, DateTime, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship


class Flight(Base):
    __tablename__ = "flights"

    id = Column(Integer, primary_key=True, autoincrement=True)
    flight_number = Column(String(5), nullable=False, unique=True)
    aircraft_id = Column(Integer, ForeignKey("aircrafts.id"), nullable=False)
    dep_airport_id = Column(Integer, ForeignKey("airports.id"), nullable=False)
    arr_airport_id = Column(Integer, ForeignKey("airports.id"), nullable=False)
    departure_time = Column(DateTime, nullable=False)
    arrival_time = Column(DateTime, nullable=False)
    economy_available_seats = Column(Integer, nullable=False)
    business_available_seats = Column(Integer, nullable=False)
    economy_price = Column(DECIMAL(10, 2), nullable=False)
    business_price = Column(DECIMAL(10, 2), nullable=False)

    aircraft = relationship("Aircraft")
    dep_airport = relationship("Airport", foreign_keys=[dep_airport_id])
    arr_airport = relationship("Airport", foreign_keys=[arr_airport_id])
    tickets = relationship("Ticket", back_populates="flight")
