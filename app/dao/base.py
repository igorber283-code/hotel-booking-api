from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession


class BaseDAO:
    model = None

    @classmethod
    async def find_all(cls, session: AsyncSession, limit=10, offset=0, **filter_by):
        stmt = select(cls.model).filter_by(**filter_by).limit(limit).offset(offset)
        result = await session.execute(stmt)
        return result.scalars().all()

    @classmethod
    async def find_one_or_none(cls, session: AsyncSession, **filter_by):
        stmt = select(cls.model).filter_by(**filter_by)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    @classmethod
    async def add(cls, session: AsyncSession, **data):
        obj = cls.model(**data)

        session.add(obj)
        await session.flush()  # получить id
        await session.refresh(obj)

        return obj

    @classmethod
    async def delete(cls, session: AsyncSession, **filter_by):
        stmt = delete(cls.model).filter_by(**filter_by)
        result = await session.execute(stmt)
        return result.rowcount or 0

    @classmethod
    async def update(cls, session: AsyncSession, filters: dict, data: dict):
        stmt = update(cls.model).filter_by(**filters).values(**data)
        result = await session.execute(stmt)
        return result.rowcount or 0
