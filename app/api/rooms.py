from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date

from app.core.database import get_session
from app.services.rooms import RoomService

router = APIRouter(prefix="/rooms", tags=["Rooms"])


@router.get("")
async def get_rooms(
    hotel_id: int | None = Query(None),
    room_id: int | None = Query(None),
    class_room: str | None = Query(None),
    price: int | None = Query(None),
    date_from: date | None = Query(None),
    date_to: date | None = Query(None),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    session: AsyncSession = Depends(get_session),
):
    return await RoomService.get_rooms(
        session=session,
        hotel_id=hotel_id,
        room_id=room_id,
        class_room=class_room,
        price=price,
        date_from=date_from,
        date_to=date_to,
        limit=limit,
        offset=offset,
    )
