import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgres+asyncpg://testuser:pwd123@db:5432/purchases"
)

Base = declarative_base()

engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    future=True,
    pool_size=20,
    max_overflow=20,
    pool_timeout=60,
)

async_session = sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
