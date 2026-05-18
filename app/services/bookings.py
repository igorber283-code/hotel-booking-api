from datetime import date

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.bookings import BookingDAO
from app.dao.rooms import RoomDAO
from app.models.rooms import Room
from app.core.redis import redis_client

from app.exceptions import (
    InvalidBookingDatesException,
    RoomNotAvailableException,
    BookingNotFoundException,
)


class BookingService:
    @classmethod
    async def add_booking(
        cls,
        session: AsyncSession,
        user_id: int,
        room_id: int,
        date_from: date,
        date_to: date,
    ):
        if date_from >= date_to:
            raise InvalidBookingDatesException(
                "Дата заезда должна быть раньше даты выезда"
            )

        room_result = await session.execute(
            select(Room).where(Room.id == room_id).with_for_update()
        )

        room = room_result.scalar_one_or_none()

        if not room:
            raise RoomNotAvailableException("Комната не найдена")

        available_rooms = await RoomDAO.find_filtered(
            session=session,
            date_from=date_from,
            date_to=date_to,
            room_id=room_id,
        )

        if not available_rooms:
            raise RoomNotAvailableException("Комната недоступна на выбранные даты")

        total_days = (date_to - date_from).days
        total_cost = total_days * room.price

        booking = await BookingDAO.add(
            session=session,
            user_id=user_id,
            room_id=room_id,
            date_from=date_from,
            date_to=date_to,
            price=room.price,
            total_days=total_days,
            total_cost=total_cost,
        )

        await session.commit()

        # Invalidate cached room lists for this hotel after booking
        async for key in redis_client.scan_iter(match=f"rooms:hotel:{room.hotel_id}:*"):
            await redis_client.delete(key)

        return booking

    @classmethod
    async def get_my_bookings(
        cls,
        session: AsyncSession,
        user_id: int,
        limit: int = 10,
        offset: int = 0,
    ):
        return await BookingDAO.find_all_by_user_id(
            session=session,
            user_id=user_id,
            limit=limit,
            offset=offset,
        )

    @classmethod
    async def delete_booking(
        cls,
        session: AsyncSession,
        booking_id: int,
        user_id: int,
    ) -> None:

        deleted = await BookingDAO.delete(
            session=session,
            id=booking_id,
            user_id=user_id,
        )

        if deleted == 0:
            raise BookingNotFoundException(
                "Бронирование не найдено или принадлежит другому пользователю"
            )

        await session.commit()
