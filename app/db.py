import os

import sqlmodel
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from sqlmodel import create_engine
from sqlmodel.ext.asyncio.session import AsyncSession, AsyncEngine

DATABASE_URL = os.getenv('DATABASE_URL')
SYNC_DATABASE_URL = os.getenv('SYNC_DATABASE_URL')

engine = AsyncEngine(create_engine(DATABASE_URL, echo=True, future=True))
sync_engine = sqlmodel.create_engine(SYNC_DATABASE_URL, echo=True)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncSession:
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
