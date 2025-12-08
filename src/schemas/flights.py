from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from decimal import Decimal
from datetime import datetime
from typing import TypedDict


class AircraftInFlightRead(BaseModel):
    tail_number: str = Field(max_length=10)
    model: str = Field(max_length=50)

    model_config = ConfigDict(from_attributes=True)


class AirportInFlightRead(BaseModel):
    code: str = Field(max_length=3)

    model_config = ConfigDict(from_attributes=True)


class FlightRead(BaseModel):
    flight_number: str = Field(max_length=5)
    aircraft: AircraftInFlightRead
    dep_airport: AirportInFlightRead
    arr_airport: AirportInFlightRead
    departure_time: datetime
    arrival_time: datetime
    economy_available_seats: int = Field(ge=0)
    business_available_seats: int = Field(ge=0)
    economy_price: Decimal = Field(ge=1)
    business_price: Decimal = Field(ge=1)

    model_config = ConfigDict(from_attributes=True)


class FlightCreate(BaseModel):
    flight_number: str = Field(max_length=5)
    aircraft_tail_number: str = Field(max_length=10)
    dep_airport_code: str = Field(max_length=3)
    arr_airport_code: str = Field(max_length=3)
    departure_time: datetime
    arrival_time: datetime
    economy_price: Decimal = Field(ge=1.0)
    business_price: Decimal = Field(ge=1.0)


class Seat(BaseModel):
    seat_class: int
    is_reserved: bool

class FlightSeatsMap(BaseModel):
    rows: list[int]
    cols: list[str]
    seats: dict[str, Seat]