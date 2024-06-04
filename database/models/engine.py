from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from config import settings
from database.models.all_models import Base

engine = create_async_engine(settings.DB_URL.get_secret_value(), echo=True)
session_maker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close_connection():
    await engine.dispose()


async def drob_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
