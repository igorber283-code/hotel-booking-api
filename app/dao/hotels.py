from sqlalchemy import select
from app.dao.base import BaseDAO
from app.models.hotels import Hotel


class HotelDAO(BaseDAO):
    model = Hotel

    @classmethod
    async def find_filtered(
        cls,
        session,
        id: int | None = None,
        name: str | None = None,
        location: str | None = None,
        rooms_count: int | None = None,
        limit: int = 10,
        offset: int = 0,
    ):
        stmt = select(cls.model)

        if id is not None:
            stmt = stmt.where(cls.model.id == id)

        if name:
            stmt = stmt.where(cls.model.name.ilike(f"%{name}%"))

        if location:
            stmt = stmt.where(cls.model.location.ilike(f"%{location}%"))

        if rooms_count is not None:
            stmt = stmt.where(cls.model.rooms_count == rooms_count)

        stmt = stmt.limit(limit).offset(offset)

        result = await session.execute(stmt)
        return result.scalars().all()
