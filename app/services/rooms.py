import json
from app.dao.rooms import RoomDAO
from app.core.redis import redis_client


class RoomService:
    @classmethod
    async def get_rooms(
        cls,
        session,
        hotel_id: int | None = None,
        room_id: int | None = None,
        class_room: str | None = None,
        price: int | None = None,
        date_from=None,
        date_to=None,
        limit: int = 10,
        offset: int = 0,
    ):
        cache_key = (
            f"rooms:{hotel_id}:{room_id}:{class_room}:"
            f"{price}:{date_from}:{date_to}:{limit}:{offset}"
        )

        cached = await redis_client.get(cache_key)
        if cached:
            return json.loads(cached)

        rooms = await RoomDAO.find_filtered(
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

        await redis_client.set(cache_key, json.dumps(rooms), ex=600)
        return rooms
