from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from db.base import Base
from db.database import conf

engine = create_async_engine(conf.db.db_url, echo=True)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
