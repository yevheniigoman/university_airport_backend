from db import Base
from sqlalchemy import Column, Integer, String, DateTime, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, autoincrement=True)
    flight_id = Column(Integer, ForeignKey("flights.id"), nullable=False)
    seat_id = Column(Integer, ForeignKey("seats.id"), nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    purchase_date = Column(DateTime, nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)
    status = Column(Integer, nullable=False)

    flight = relationship("Flight", back_populates="tickets")
    seat = relationship("Seat")