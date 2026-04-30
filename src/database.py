from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from src.settings import Settings

engine = create_async_engine(Settings().DATABASE_URL)
# table_registry.metadata.create_all(engine)


async def get_session():
    async with AsyncSession(
        engine, expire_on_commit=False
    ) as session:  # pragma: no cover
        yield session
