from models import Flight, Airport, Aircraft, Seat
from schemas.flights import FlightCreate
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

class FlightService():
    @staticmethod
    def create_flight(session: Session, flight: FlightCreate) -> Flight:
        dep_airport = session.query(Airport).filter_by(code=flight.dep_airport_code).first()
        arr_airport = session.query(Airport).filter_by(code=flight.arr_airport_code).first()
        if not dep_airport or not arr_airport:
            raise ValueError("Invalid airport code")

        aircraft = session.query(Aircraft).filter_by(tail_number=flight.aircraft_tail_number).first()
        if not aircraft:
            raise ValueError("Invalid aircraft tail number.")

        if not isinstance(flight.departure_time, datetime):
            raise TypeError("departure_time must be datetime.")

        if not isinstance(flight.arrival_time, datetime):
            raise TypeError("arrival_time must be datetime.")

        if flight.arrival_time <= flight.departure_time:
            raise ValueError("Arrival time must be greater than departure time.")

        seats = session.query(Seat).filter_by(aircraft_id=aircraft.id).all()
        if len(seats) == 0:
            raise ValueError(f"No seats found for aircraft {flight.aircraft_tail_number}.")
        economy_count = len([s for s in seats if s.seat_class == 2])
        business_count = len([s for s in seats if s.seat_class == 1])

        # Creating Flight object
        flight = Flight(
            flight_number=flight.flight_number,
            aircraft=aircraft,
            dep_airport=dep_airport,
            arr_airport=arr_airport,
            departure_time=flight.departure_time,
            arrival_time=flight.arrival_time,
            economy_available_seats=economy_count,
            business_available_seats=business_count,
            economy_price=flight.economy_price,
            business_price=flight.business_price
        )
        return flight

    @staticmethod
    def get_duration(flight: Flight) -> float:
        delta = flight.arrival_time - flight.departure_time
        return delta.total_seconds() / 3600

    @classmethod
    def calculate_fuel(cls, flight: Flight) -> float:
        duration = cls.get_duration(flight)
        return float(flight.aircraft.fuel_per_hour) * duration

    @staticmethod
    def get_upcoming(session: Session, hours: int = 2):
        now = datetime.now()
        until = now + timedelta(hours=hours)

        flights = session.query(Flight).filter(
            Flight.departure_time >= now,
            Flight.departure_time <= until
        ).all()

        return flights

    @staticmethod
    def get_by_number(session: Session, flight_number: str):
        flight = session.query(Flight).filter(Flight.flight_number == flight_number).first()
        return flight
