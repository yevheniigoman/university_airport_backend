from models import Flight, Airport, Aircraft, Seat
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

class FlightService():
    def __init__(self, session: Session):
        self.session = session

    def create_flight(
            self,
            flight_number: str,
            dep_code: str,
            arr_code: str,
            aircraft_id: int,
            departure_time: datetime,
            arrival_time: datetime,
            economy_price: float,
            business_price: float
    ):

        dep_airport = self.session.query(Airport).filter_by(code=dep_code).first()
        arr_airport = self.session.query(Airport).filter_by(code=arr_code).first()
        if not dep_airport or not arr_airport:
            raise ValueError("Invalid airport code")

        aircraft = self.session.query(Aircraft).filter_by(id=aircraft_id).first()
        if not aircraft:
            raise ValueError("Invalid aircraft ID")

        if not isinstance(departure_time, datetime):
            raise TypeError("departure_time must be datetime")

        if not isinstance(arrival_time, datetime):
            raise TypeError("arrival_time must be datetime")

        if arrival_time <= departure_time:
            arrival_time = arrival_time + timedelta(days=1)

        seats = self.session.query(Seat).filter_by(aircraft_id=aircraft_id).all()
        if len(seats) == 0:
            raise ValueError(f"No seats found for aircraft ID {aircraft_id}. "
                             f"Please generate seats using AircraftService before creating a flight")
        economy_count = len([s for s in seats if s.seat_class == 2])
        business_count = len([s for s in seats if s.seat_class == 1])

        # Creating Flight object
        flight = Flight(
            flight_number=flight_number,
            aircraft_id=aircraft_id,
            dep_airport=dep_airport,
            arr_airport=arr_airport,
            departure_time=departure_time,
            arrival_time=arrival_time,
            economy_available_seats=economy_count,
            business_available_seats=business_count,
            economy_price=economy_price,
            business_price=business_price)

        self.session.add(flight)
        self.session.commit()
        return flight

    @classmethod
    def get_duration(cls, flight: Flight) -> float:
        delta = flight.arrival_time - flight.departure_time
        return delta.total_seconds() / 3600


    @classmethod
    def calculate_fuel(cls, flight: Flight) -> float:
        duration = cls.get_duration(flight)
        return float(flight.aircraft.fuel_per_hour) * duration


    def get_upcoming(self, hours: int=2):
        now = datetime.now()
        until = now + timedelta(hours=hours)

        flights = self.session.query(Flight).filter(
            Flight.departure_time >= now,
            Flight.departure_time <= until
        ).all()

        return flights


    def get_by_number(self, flight_number: str):
        flight = self.session.query(Flight).filter(Flight.flight_number == flight_number).first()
        return flight
