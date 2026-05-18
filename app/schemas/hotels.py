from pydantic import BaseModel, ConfigDict


class SHotel(BaseModel):
    id: int
    name: str
    location: str
    rooms_count: int

    model_config = ConfigDict(from_attributes=True)
