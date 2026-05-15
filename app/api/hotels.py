from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.dao.hotels import HotelDAO
from app.schemas.hotels import SHotel

router = APIRouter(
    prefix="/hotels",
    tags=["Hotels"],
)


@router.get("", response_model=list[SHotel])
async def get_hotels(
    id: int | None = Query(None),
    name: str | None = Query(None),
    location: str | None = Query(None),
    rooms_count: int | None = Query(None),
    limit: int = Query(10),
    offset: int = Query(0),
    session: AsyncSession = Depends(get_session),
):
    return await HotelDAO.find_filtered(
        session=session,
        id=id,
        name=name,
        location=location,
        rooms_count=rooms_count,
        limit=limit,
        offset=offset,
    )
