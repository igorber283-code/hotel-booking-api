import asyncio
import pytest_asyncio
from unittest.mock import AsyncMock

from httpx import AsyncClient, ASGITransport

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from app.main import app
from app.core.config import settings
from app.core.database import Base, get_session
from app.models.hotels import Hotel
from app.models.rooms import Room


@pytest_asyncio.fixture(autouse=True)
async def mock_redis(monkeypatch):
    fake_redis = AsyncMock()

    fake_redis.get.return_value = None
    fake_redis.set.return_value = True
    fake_redis.delete.return_value = 1

    async def scan_iter(*args, **kwargs):
        if False:
            yield None

    fake_redis.scan_iter = scan_iter

    monkeypatch.setattr(
        "app.services.bookings.redis_client",
        fake_redis,
    )

    yield


engine_test = create_async_engine(
    settings.TEST_DATABASE_URL,
    echo=False,
    poolclass=NullPool,
)

AsyncTestSession = sessionmaker(
    bind=engine_test,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def override_get_session():
    async with AsyncTestSession() as session:
        yield session


app.dependency_overrides[get_session] = override_get_session


@pytest_asyncio.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine_test.dispose()


@pytest_asyncio.fixture
async def ac():
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as client:
        yield client


@pytest_asyncio.fixture
async def db_session():
    async with AsyncTestSession() as session:
        yield session
        await session.rollback()


@pytest_asyncio.fixture
async def test_hotel(db_session):
    hotel = Hotel(
        name="Test Hotel",
        location="Stockholm",
        rooms_count=5,
    )
    db_session.add(hotel)
    await db_session.commit()
    await db_session.refresh(hotel)
    return hotel


@pytest_asyncio.fixture
async def test_room(db_session, test_hotel):
    room = Room(
        hotel_id=test_hotel.id,
        count_room=1,
        class_room="lux",
        price=1000,
    )
    db_session.add(room)
    await db_session.commit()
    await db_session.refresh(room)
    return room
