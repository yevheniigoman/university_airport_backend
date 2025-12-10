from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


class CityInRouteRead(BaseModel):
    name: str = Field(max_length=50)

    model_config = ConfigDict(from_attributes=True)


class AirportInRouteRead(BaseModel):
    name: str = Field(max_length=100)
    code: str = Field(max_length=3)
    city: CityInRouteRead

    model_config = ConfigDict(from_attributes=True)


class FlightInRouteRead(BaseModel):
    flight_number: str
    dep_airport: AirportInRouteRead
    arr_airport: AirportInRouteRead
    departure_time: datetime
    arrival_time: datetime

    model_config = ConfigDict(from_attributes=True)


class RouteRead(BaseModel):
    flights: list[FlightInRouteRead]
