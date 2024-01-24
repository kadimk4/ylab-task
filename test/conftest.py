import pytest, asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from httpx import AsyncClient

from config import DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME
from main import app
from models.menu import metadata

test_engine = create_async_engine(f'postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}', echo=False)
async_session_maker = async_sessionmaker(bind=test_engine, expire_on_commit=False)
metadata.bind = test_engine


async def override_get_async_db():
    async with async_session_maker() as session:
        yield session


app.dependency_overrides[override_get_async_db] = override_get_async_db


@pytest.fixture(autouse=True, scope='session')
async def prepare_db():
    async with test_engine.begin() as conn:
        await conn.run_sync(metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(metadata.drop_all)


@pytest.fixture(scope='session')
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


client = TestClient(app)


@pytest.fixture(scope='session')
async def ac():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac