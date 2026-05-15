import asyncio
from app.core.config import settings

import pytest_asyncio

from httpx import AsyncClient, ASGITransport

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
)

from sqlalchemy.pool import NullPool

from app.main import app
from app.core.database import Base, get_session

from app.models.hotels import Hotel
from app.models.rooms import Room


TEST_DATABASE_URL = settings.TEST_DATABASE_URL


engine_test = create_async_engine(
    TEST_DATABASE_URL,
    echo=False,
    poolclass=NullPool,
)

TestSession = async_sessionmaker(
    bind=engine_test,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def override_get_session():
    async with TestSession() as session:
        yield session


app.dependency_overrides[get_session] = override_get_session


@pytest_asyncio.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def prepare_db():

    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine_test.dispose()


@pytest_asyncio.fixture
async def session():

    async with TestSession() as session:
        yield session


@pytest_asyncio.fixture
async def ac():

    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as client:
        yield client


@pytest_asyncio.fixture
async def test_hotel(session):

    hotel = Hotel(
        name="Test Hotel",
        location="Stockholm",
        rooms_count=5,
    )

    session.add(hotel)

    await session.commit()
    await session.refresh(hotel)

    return hotel


@pytest_asyncio.fixture
async def test_room(session, test_hotel):

    room = Room(
        hotel_id=test_hotel.id,
        count_room=1,
        class_room="lux",
        price=1000,
    )

    session.add(room)

    await session.commit()
    await session.refresh(room)

    return room
