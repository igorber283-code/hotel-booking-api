from sqlalchemy import select, func

from app.dao.base import BaseDAO
from app.models.bookings import Booking


class BookingDAO(BaseDAO):
    model = Booking

    @classmethod
    def booked_rooms_cte(cls, date_from, date_to):
        return (
            select(
                Booking.room_id.label("room_id"),
                func.count(Booking.room_id).label("rooms_booked"),
            )
            .where(
                Booking.date_from <= date_to,
                Booking.date_to >= date_from,
            )
            .group_by(Booking.room_id)
            .cte("booked_rooms")
        )

    @classmethod
    async def find_all_by_user_id(
        cls,
        session,
        user_id: int,
        limit: int = 10,
        offset: int = 0,
    ):
        stmt = (
            select(cls.model)
            .where(cls.model.user_id == user_id)
            .order_by(cls.model.id.desc())
            .limit(limit)
            .offset(offset)
        )

        result = await session.execute(stmt)
        return result.scalars().all()
