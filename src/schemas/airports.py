from pydantic import BaseModel, Field, ConfigDict


class AirportRead(BaseModel):
    name: str = Field(max_length=100)
    code: str = Field(max_length=3)
    city_id: int = Field(ge=1)

    model_config = ConfigDict(from_attributes=True)