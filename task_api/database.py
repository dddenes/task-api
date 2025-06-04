"""Database configuration
"""

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from task_api import config

engine: AsyncEngine = create_async_engine(config.SQLALCHEMY_URL, echo=True)
async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_session() -> AsyncSession:
    """Yields a session for DB queries"""

    async with async_session() as session:
        yield session
