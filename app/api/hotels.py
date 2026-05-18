from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.services.hotels import HotelService

router = APIRouter(prefix="/hotels", tags=["Hotels"])


@router.get("")
async def get_hotels(
    id: int | None = Query(None),
    name: str | None = Query(None),
    location: str | None = Query(None),
    rooms_count: int | None = Query(None),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    session: AsyncSession = Depends(get_session),
):
    return await HotelService.get_hotels(
        session=session,
        id=id,
        name=name,
        location=location,
        rooms_count=rooms_count,
        limit=limit,
        offset=offset,
    )
