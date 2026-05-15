from pydantic import BaseModel, ConfigDict


class SRoomInfo(BaseModel):
    id: int
    hotel_id: int
    class_room: str
    price: int
    count_room: int
    rooms_left: int

    model_config = ConfigDict(from_attributes=True)
