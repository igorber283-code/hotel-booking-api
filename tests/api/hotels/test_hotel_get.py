import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_hotels_list(ac: AsyncClient, test_hotel):

    response = await ac.get("/hotels")

    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, list)
    assert len(data) >= 1
    assert any(
        hotel["name"] == "Test Hotel" and hotel["location"] == "Stockholm"
        for hotel in data
    )
