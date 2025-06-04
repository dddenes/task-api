"""Fixtures, that can be used accross all unittests
"""

import pytest_asyncio

from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from task_api import config
from task_api.app import create_app
from task_api.database import get_session
from task_api.models import Base

test_engine = create_async_engine(config.SQLALCHEMY_URL, echo=False, future=True)
TestSessionLocal = sessionmaker(bind=test_engine, class_=AsyncSession, expire_on_commit=False)


@pytest_asyncio.fixture
def app():
    """Fixture to create the FastAPI object for the tests
    """
    app_instance = create_app()

    return app_instance  # ezzel biztosítod, hogy add_pagination is lefut


# Ez fogja helyettesíteni a get_session-t a tesztek idejére
@pytest_asyncio.fixture
async def override_get_session():
    """Fixture to override the original sessions to conform the testing env
    """
    async def _override_get_session():
        async with TestSessionLocal() as session:
            yield session

    return _override_get_session


# Adatbázis inicializálás minden teszt futása előtt
@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_test_db():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def async_client(override_get_session, app):
    app.dependency_overrides[get_session] = override_get_session

    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
