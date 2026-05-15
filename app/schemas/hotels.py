from pydantic import BaseModel


class SHotel(BaseModel):
    id: int
    name: str
    location: str
    rooms_count: int
