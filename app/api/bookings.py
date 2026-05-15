from datetime import date
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from authx import TokenPayload

from app.core.database import get_session
from app.core.security import security
from app.schemas.bookings import BookingResponse
from app.services.bookings import BookingService

router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.post("/{room_id}", status_code=status.HTTP_201_CREATED)
async def add_booking(
    room_id: int,
    date_from: date = Query(...),
    date_to: date = Query(...),
    session: AsyncSession = Depends(get_session),
    token_payload: TokenPayload = Depends(security.access_token_required),
) -> BookingResponse:

    current_user_id = int(token_payload.sub)

    return await BookingService.add_booking(
        session=session,
        user_id=current_user_id,
        room_id=room_id,
        date_from=date_from,
        date_to=date_to,
    )


@router.get("/me")
async def get_my_bookings(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    session: AsyncSession = Depends(get_session),
    token_payload: TokenPayload = Depends(security.access_token_required),
):

    current_user_id = int(token_payload.sub)

    return await BookingService.get_my_bookings(
        session=session,
        user_id=current_user_id,
        limit=limit,
        offset=offset,
    )


@router.delete("/{booking_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_booking(
    booking_id: int,
    session: AsyncSession = Depends(get_session),
    token_payload: TokenPayload = Depends(security.access_token_required),
):
    current_user_id = int(token_payload.sub)

    await BookingService.delete_booking(
        session=session,
        booking_id=booking_id,
        user_id=current_user_id,
    )
