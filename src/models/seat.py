from db import Base
from sqlalchemy import Column, Integer, String, UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship


class Seat(Base):
    __tablename__ = "seats"

    id = Column(Integer, primary_key=True, autoincrement=True)
    aircraft_id = Column(Integer, ForeignKey("aircrafts.id"), nullable=False)
    seat_number = Column(String(3), nullable=False)
    # class: 1, 2
    seat_class = Column(Integer, nullable=False)

    aircraft = relationship("Aircraft", back_populates="seats")

    # to prevent same seats numbers in one aircraft
    __table_args__ = (
        UniqueConstraint("aircraft_id", "seat_number", name="uix_seat_aircraft"),
    )
