from sqlalchemy import select, func
from app.dao.base import BaseDAO
from app.models.rooms import Room
from app.dao.bookings import BookingDAO
from datetime import date


class RoomDAO(BaseDAO):
    model = Room

    @classmethod
    async def find_filtered(
        cls,
        session,
        hotel_id: int | None = None,
        room_id: int | None = None,
        class_room: str | None = None,
        price: int | None = None,
        date_from: date | None = None,
        date_to: date | None = None,
        limit: int = 10,
        offset: int = 0,
    ):
        stmt = select(
            cls.model.id,
            cls.model.hotel_id,
            cls.model.count_room,
            cls.model.class_room,
            cls.model.price,
        )

        if hotel_id is not None:
            stmt = stmt.where(cls.model.hotel_id == hotel_id)

        if room_id is not None:
            stmt = stmt.where(cls.model.id == room_id)

        if class_room is not None:
            stmt = stmt.where(cls.model.class_room == class_room)

        if price is not None:
            stmt = stmt.where(cls.model.price == price)

        if date_from is not None and date_to is not None:
            booked_rooms = BookingDAO.booked_rooms_cte(date_from, date_to)

            rooms_left_calc = cls.model.count_room - func.coalesce(
                booked_rooms.c.rooms_booked, 0
            )

            stmt = (
                stmt.outerjoin(
                    booked_rooms,
                    booked_rooms.c.room_id == cls.model.id,
                )
                .where(rooms_left_calc > 0)
                .add_columns(rooms_left_calc.label("rooms_left"))
            )
        else:
            stmt = stmt.add_columns(cls.model.count_room.label("rooms_left"))

        stmt = stmt.limit(limit).offset(offset)

        result = await session.execute(stmt)
        return result.mappings().all()
