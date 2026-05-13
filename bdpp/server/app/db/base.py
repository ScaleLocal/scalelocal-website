"""SQLAlchemy async engine + session."""
from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from ..settings import get_settings


class Base(DeclarativeBase):
    pass


settings = get_settings()
engine = create_async_engine(settings.database_url, echo=False, future=True)
SessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_session() -> AsyncSession:
    async with SessionLocal() as session:
        yield session


async def init_db():
    """Create tables if they don't exist (dev convenience; Alembic for prod migrations)."""
    from . import models  # noqa: F401 to register models
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
