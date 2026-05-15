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

    token = login_response.json()["access_token"]

    booking_response = await ac.post(
        f"/bookings/{test_room.id}?date_from=2026-11-11&date_to=2026-11-16",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert booking_response.status_code == 201

    data = booking_response.json()

    assert data["room_id"] == test_room.id
    assert data["price"] == 1000
    assert data["total_days"] == 5
    assert data["total_cost"] == 5000


@pytest.mark.asyncio
async def test_get_my_bookings(ac, test_room):

    await ac.post(
        "/authx/register",
        json={
            "email": "my_bookings@example.com",
            "password": "password123",
        },
    )

    login_response = await ac.post(
        "/authx/login",
        json={
            "email": "my_bookings@example.com",
            "password": "password123",
        },
    )

    token = login_response.json()["access_token"]

    await ac.post(
        f"/bookings/{test_room.id}?date_from=2026-12-01&date_to=2026-12-05",
        headers={"Authorization": f"Bearer {token}"},
    )

    response = await ac.get(
        "/bookings/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) > 0

    booking = data[0]

    assert booking["room_id"] == test_room.id


@pytest.mark.asyncio
async def test_delete_booking(ac, test_room):

    await ac.post(
        "/authx/register",
        json={
            "email": "delete_booking@example.com",
            "password": "password123",
        },
    )

    login_response = await ac.post(
        "/authx/login",
        json={
            "email": "delete_booking@example.com",
            "password": "password123",
        },
    )

    token = login_response.json()["access_token"]

    booking_response = await ac.post(
        f"/bookings/{test_room.id}?date_from=2026-10-01&date_to=2026-10-05",
        headers={"Authorization": f"Bearer {token}"},
    )

    booking_id = booking_response.json()["id"]

    delete_response = await ac.delete(
        f"/bookings/{booking_id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert delete_response.status_code == 204


@pytest.mark.asyncio
async def test_create_booking_with_invalid_dates(ac, test_room):

    await ac.post(
        "/authx/register",
        json={
            "email": "invalid_dates@example.com",
            "password": "password123",
        },
    )

    login_response = await ac.post(
        "/authx/login",
        json={
            "email": "invalid_dates@example.com",
            "password": "password123",
        },
    )

    token = login_response.json()["access_token"]

    response = await ac.post(
        f"/bookings/{test_room.id}?date_from=2026-11-20&date_to=2026-11-10",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 400
