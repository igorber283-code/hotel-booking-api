import asyncio
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_booking_stress_load(ac: AsyncClient, test_room):

    user_data = {"email": "stress_test@example.com", "password": "Password123!"}
    await ac.post("/authx/register", json=user_data)
    login_res = await ac.post("/authx/login", json=user_data)
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    params = {"date_from": "2026-12-15", "date_to": "2026-12-20"}

    async def create_booking():
        return await ac.post(
            f"/bookings/{test_room.id}", params=params, headers=headers
        )

    tasks = [create_booking() for _ in range(50)]

    results = await asyncio.gather(*tasks, return_exceptions=True)

    status_codes = [
        res.status_code for res in results if not isinstance(res, Exception)
    ]

    success_count = status_codes.count(201)
    conflict_count = status_codes.count(409)
    other_errors = len(results) - success_count - conflict_count
    print("==========ИТОГИ ТЕСТА==========")
    print(f"Успешно (201): {success_count}")
    print(f"Конфликтов (409): {conflict_count}")
    print(f"Прочих ошибок/исключений: {other_errors}")

    assert success_count == 1, f"Должна быть только 1 бронь, но их {success_count}!"
    assert success_count + conflict_count == 50
