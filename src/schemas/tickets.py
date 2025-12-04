from pydantic import BaseModel, ConfigDict, Field
from decimal import Decimal


class FlightInTicketRead(BaseModel):
    flight_number: str = Field(max_length=5)

    model_config = ConfigDict(from_attributes=True)


class SeatInTicketRead(BaseModel):
    seat_number: str = Field(max_length=3)
    seat_class: int = Field(ge=1, le=2)

    model_config = ConfigDict(from_attributes=True)


class TicketRead(BaseModel):
    flight: FlightInTicketRead
    seat: SeatInTicketRead
    price: Decimal
    status: int = Field(ge=0, le=1)

    model_config = ConfigDict(from_attributes=True)