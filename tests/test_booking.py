import pytest


@pytest.mark.asyncio
async def test_create_booking(ac, test_room):

    await ac.post(
        "/authx/register",
        json={
            "email": "booking_test@example.com",
            "password": "password123",
        },
    )

    login_response = await ac.post(
        "/authx/login",
        json={
            "email": "booking_test@example.com",
            "password": "password123",
        },
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    booking_response = await ac.post(
        f"/bookings/{test_room.id}?date_from=2026-11-11&date_to=2026-11-16",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert booking_response.status_code == 201, booking_response.text

    data = booking_response.json()

    assert data["room_id"] == test_room.id
    assert data["price"] == 1000
    assert data["total_days"] == 5
    assert data["total_cost"] == 5000

    assert data["date_from"] == "2026-11-11"
    assert data["date_to"] == "2026-11-16"
