from pydantic import BaseModel, Field, ConfigDict
from decimal import Decimal


class AircraftRead(BaseModel):
    tail_number: str = Field(max_length=10)
    model: str = Field(max_length=50)
    fuel_per_hour: Decimal = Field(gt=0)
    total_seats: int = Field(ge=1)

    model_config = ConfigDict(from_attributes=True)
