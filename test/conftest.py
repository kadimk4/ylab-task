import asyncio
from typing import AsyncGenerator

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool


from config import (DB_HOST, DB_NAME, DB_PASS, DB_PORT,
                        DB_USER)
from main import app

from src.db.database import get_async_db
from src.db.models import metadata, Menu, Submenu, Dishes

# DATABASE
db_url_test = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine_test = create_async_engine(db_url_test, poolclass=NullPool)
async_session_maker = sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)
metadata.bind = engine_test


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

app.dependency_overrides[get_async_db] = override_get_async_session


@pytest.fixture(autouse=True, scope='session')
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(metadata.drop_all)

# SETUP


@pytest.fixture(scope='session')
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


client = TestClient(app)


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="session")
async def menu_id_fixture(ac: AsyncClient):
    menu_response = await ac.post('/api/v1/menus/', json={
        "title": "My menu 1",
        "description": "My menu description 1"
    })
    assert menu_response.status_code == 201
    menu_id = menu_response.json()['id']

    async with async_session_maker() as session:
        stmt = select(Menu).filter(Menu.uuid == menu_id)
        result = await session.execute(stmt)
        menu = result.scalar()
        assert menu is not None

    return menu


@pytest.fixture(scope="session")
async def submenu_id_fixture(ac: AsyncClient):
    menu_response = await ac.post('/api/v1/menus/', json={
        "title": "My menu 1",
        "description": "My menu description 1"
    })
    assert menu_response.status_code == 201
    menu_id = menu_response.json()['id']

    async with async_session_maker() as session:
        stmt = select(Menu).filter(Menu.uuid == menu_id)
        result = await session.execute(stmt)
        menu = result.scalar()
        assert menu is not None

    submenu_response = await ac.post(f'/api/v1/menus/{menu_id}/submenus/', json={
        "title": "My submenu 1",
        "description": "My submenu description 1"
    })
    assert submenu_response.status_code == 201
    submenu_id = submenu_response.json()['id']

    async with async_session_maker() as session:
        stmt = select(Submenu).filter(Submenu.uuid == submenu_id)
        result = await session.execute(stmt)
        submenu = result.scalar()
        assert submenu is not None

    return menu, submenu


@pytest.fixture(scope="session")
async def dish_id_fixture(ac: AsyncClient):
    menu_response = await ac.post('/api/v1/menus/', json={
        "title": "My menu 1",
        "description": "My menu description 1"
    })
    assert menu_response.status_code == 201
    menu_id = menu_response.json()['id']

    async with async_session_maker() as session:
        stmt = select(Menu).filter(Menu.uuid == menu_id)
        result = await session.execute(stmt)
        menu = result.scalar()
        assert menu is not None

    submenu_response = await ac.post(f'/api/v1/menus/{menu_id}/submenus/', json={
        "title": "My submenu 1",
        "description": "My submenu description 1"
    })
    assert submenu_response.status_code == 201
    submenu_id = submenu_response.json()['id']

    async with async_session_maker() as session:
        stmt = select(Submenu).filter(Submenu.uuid == submenu_id)
        result = await session.execute(stmt)
        submenu = result.scalar()
        assert submenu is not None

    dish_response = await ac.post(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/', json={
        "title": "My dish 1",
        "description": "My dish description 1",
        "price": "12.50"
    })
    assert dish_response.status_code == 201
    dish_id = dish_response.json()['id']
    async with async_session_maker() as session:
        stmt = select(Dishes).filter(Dishes.uuid == dish_id)
        result = await session.execute(stmt)
        dish = result.scalar()
        assert dish is not None

    return menu, submenu, dish
