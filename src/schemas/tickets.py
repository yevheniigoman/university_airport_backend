from pydantic import BaseModel, Field
from dataclasses import dataclass


@dataclass
class Passenger:
    first_name: str
    last_name: str


class TicketCreate(BaseModel):
    flight_number: str = Field(max_length=5)
    seat_number: str = Field(max_length=3)
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
