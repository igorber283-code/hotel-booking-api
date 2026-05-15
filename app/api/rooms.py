from datetime import date
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.dao.rooms import RoomDAO
from app.schemas.rooms import SRoomInfo
from app.exceptions import RoomNotAvailableException

router = APIRouter(prefix="/rooms", tags=["Rooms"])


@router.get("/rooms", response_model=list[SRoomInfo])
async def get_rooms(
    hotel_id: int | None = Query(None),
    class_room: str | None = Query(None),
    price: int | None = Query(None),
    date_from: date | None = Query(None),
    date_to: date | None = Query(None),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    session: AsyncSession = Depends(get_session),
):
    rooms = await RoomDAO.find_filtered(
        session=session,
        hotel_id=hotel_id,
        class_room=class_room,
        price=price,
        date_from=date_from,
        date_to=date_to,
        limit=limit,
        offset=offset,
    )

    if not rooms:
        raise RoomNotAvailableException()

    return rooms
