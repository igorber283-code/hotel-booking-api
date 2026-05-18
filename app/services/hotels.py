import json
from app.dao.hotels import HotelDAO
from app.core.redis import redis_client
from app.schemas.hotels import SHotel


class HotelService:
    @classmethod
    async def get_hotels(
        cls,
        session,
        id: int | None = None,
        name: str | None = None,
        location: str | None = None,
        rooms_count: int | None = None,
        limit: int = 10,
        offset: int = 0,
    ):
        cache_key = f"hotels:{id}:{name}:{location}:{rooms_count}:{limit}:{offset}"

        cached = await redis_client.get(cache_key)
        if cached:
            return json.loads(cached)

        hotels = await HotelDAO.find_filtered(
            session=session,
            id=id,
            name=name,
            location=location,
            rooms_count=rooms_count,
            limit=limit,
            offset=offset,
        )

        hotels_data = [SHotel.model_validate(h).model_dump() for h in hotels]

        await redis_client.set(cache_key, json.dumps(hotels_data), ex=600)
        return hotels_data
