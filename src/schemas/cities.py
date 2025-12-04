from pydantic import BaseModel, Field, ConfigDict


class CityRead(BaseModel):
    id: int = Field(ge=1)
    name: str = Field(max_length=50)

    model_config = ConfigDict(from_attributes=True)