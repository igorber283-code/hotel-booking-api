import asyncio
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_booking_race_condition(ac: AsyncClient, test_room):

    user_data = {"email": "race_test@example.com", "password": "Password123!"}
    await ac.post("/authx/register", json=user_data)
    login_res = await ac.post("/authx/login", json=user_data)
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    params = {"date_from": "2026-12-01", "date_to": "2026-12-10"}

    async def create_booking():
        return await ac.post(
            f"/bookings/{test_room.id}",
            params=params,
            headers=headers,
        )

    results = await asyncio.gather(
        create_booking(),
        create_booking(),
        return_exceptions=True,
    )

    status_codes = [res.status_code for res in results]

    success_count = status_codes.count(201)
    fail_count = status_codes.count(409)

    assert success_count == 1
    assert fail_count == 1

    my_bookings = await ac.get("/bookings/me", headers=headers)
    assert len(my_bookings.json()) == 1
