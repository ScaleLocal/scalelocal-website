"""SQLAlchemy async engine + session."""
from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from ..settings import get_settings


class Base(DeclarativeBase):
    pass


def _coerce_async_url(url: str) -> str:
    """Render gives us `postgresql://...`; SQLAlchemy async needs `postgresql+asyncpg://...`."""
    if not url:
        return url
    if url.startswith("postgres://"):
        url = "postgresql://" + url[len("postgres://"):]
    if url.startswith("postgresql://") and "+asyncpg" not in url:
        url = "postgresql+asyncpg://" + url[len("postgresql://"):]
    return url


settings = get_settings()
DATABASE_URL = _coerce_async_url(settings.database_url)
engine = create_async_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_session() -> AsyncSession:
    async with SessionLocal() as session:
        yield session


async def init_db():
    """Create tables if they don't exist (dev convenience; Alembic for prod migrations)."""
    from . import models  # noqa: F401
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
