from pydantic import BaseModel, Field, ConfigDict


class CityInAirportRead(BaseModel):
    name: str = Field(max_length=50)


class AirportRead(BaseModel):
    name: str = Field(max_length=100)
    code: str = Field(max_length=3)
    city: CityInAirportRead

    model_config = ConfigDict(from_attributes=True)