import pytest
from httpx import AsyncClient
from src.db.models import Menu
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from conftest import async_session_maker


@pytest.mark.asyncio
async def test_menu_crud(ac: AsyncClient, menu_id_fixture):

    response = await ac.get('/api/v1/menus/')
    assert response.status_code == 200
    assert len(response.json()) == 1

    menu_id = menu_id_fixture.uuid
    response = await ac.get(f'/api/v1/menus/{menu_id}')
    assert response.status_code == 200
    assert response.json()['id'] == str(menu_id)
    assert response.json()['title'] == "My menu 1"
    assert response.json()['description'] == "My menu description 1"
    assert response.json()['submenus_count'] == 0
    assert response.json()['dishes_count'] == 0

    updated_title = "Updated Menu"
    updated_desc = "Updated Menu Description"
    response = await ac.patch(f'/api/v1/menus/{menu_id}', json={"title": updated_title, "description": updated_desc})
    assert response.status_code == 200
    assert response.json()['title'] == updated_title
    assert response.json()['description'] == updated_desc
    assert response.json()['submenus_count'] == 0
    assert response.json()['dishes_count'] == 0

    async with async_session_maker() as db:
        menu = await db.execute(select(Menu).filter(Menu.uuid == menu_id))
        menu_data = menu.scalar()
        assert menu_data.title == updated_title
        assert menu_data.description == updated_desc

    response = await ac.delete(f'/api/v1/menus/{menu_id}')
    assert response.status_code == 200
    assert response.json()['id'] == str(menu_id)
    assert response.json()['title'] == updated_title
    assert response.json()['description'] == updated_desc
    assert response.json()['submenus_count'] == 0
    assert response.json()['dishes_count'] == 0

    async with async_session_maker() as db:
        menu = await db.execute(select(Menu).filter(Menu.uuid == menu_id))
        assert menu.scalar() is None


@pytest.mark.asyncio
async def test_menu_post(ac: AsyncClient):

    new_title = "My menu 1"
    new_desc = "My menu 1 description"
    response = await ac.post('/api/v1/menus/', json={"title": new_title, "description": new_desc})
    assert response.status_code == 201
    assert response.json()['title'] == new_title
    assert response.json()['description'] == new_desc

    async with async_session_maker() as db:
        menu = await db.execute(select(Menu).filter(Menu.title == new_title))
        assert menu.scalar() is not None
