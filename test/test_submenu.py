import pytest
from httpx import AsyncClient
from sqlalchemy import select
from models.menu import Submenu
from conftest import async_session_maker


@pytest.mark.asyncio
async def test_submenu_crud(ac: AsyncClient, submenu_id_fixture, menu_id_fixture):
    menu, submenu = submenu_id_fixture
    menu_id, submenu_id = menu.uuid, submenu.uuid
    response = await ac.get(f'/api/v1/menus/{menu_id}/submenus/')
    assert response.status_code == 200
    assert len(response.json()) == 1

    response = await ac.get(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}')
    assert response.status_code == 200
    assert response.json()['id'] == str(submenu_id)
    assert response.json()['title'] == "My submenu 1"
    assert response.json()['description'] == "My submenu description 1"
    assert response.json()['menu_id'] == str(menu_id)
    assert response.json()['dishes_count'] == 0

    updated_title = "Updated Submenu"
    updated_desc = "Updated Submenu Description"
    response = await ac.patch(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}', json={"title": updated_title, "description": updated_desc})
    assert response.status_code == 200
    assert response.json()['title'] == updated_title
    assert response.json()['description'] == updated_desc
    assert response.json()['menu_id'] == str(menu_id)
    assert response.json()['dishes_count'] == 0

    async with async_session_maker() as db:
        submenu = await db.execute(select(Submenu).filter(Submenu.uuid == submenu_id))
        submenu_data = submenu.scalar()
        assert submenu_data.title == updated_title
        assert submenu_data.description == updated_desc

    response = await ac.delete(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}')
    assert response.status_code == 200
    assert response.json()['id'] == str(submenu_id)
    assert response.json()['title'] == updated_title
    assert response.json()['description'] == updated_desc
    assert response.json()['menu_id'] == str(menu_id)
    assert response.json()['dishes_count'] == 0

    async with async_session_maker() as db:
        submenu = await db.execute(select(Submenu).filter(Submenu.uuid == submenu_id))
        assert submenu.scalar() is None

@pytest.mark.asyncio
async def test_submenu_post(ac: AsyncClient, menu_id_fixture):
    menu_id = menu_id_fixture.uuid
    new_title = "My submenu 1"
    new_desc = "My submenu 1 description"
    response = await ac.post(f'/api/v1/menus/{menu_id}/submenus/',
                             json={"title": new_title, "description": new_desc})
    assert response.status_code == 201
    assert response.json()['title'] == new_title
    assert response.json()['description'] == new_desc
    assert response.json()['menu_id'] == str(menu_id)

    async with async_session_maker() as db:
        submenu = await db.execute(select(Submenu).filter(Submenu.title == new_title))
        assert submenu.scalar() is not None
