import pytest
from httpx import AsyncClient
from sqlalchemy import select

from conftest import async_session_maker
from models.menu import Menu, Submenu


class TestSubmenus:
    menu_id = None
    submenu_id = None

    @classmethod
    @pytest.mark.asyncio
    async def test_create_menu(cls, ac: AsyncClient):
        async with async_session_maker() as db:
            menu = await ac.post('/api/v1/menus/', json={
                "title": "My menu 1",
                "description": "My menu description 1"
            })
            assert menu.status_code == 201
            cls.menu_id = menu.json()["id"]
            query = select(Menu).where(Menu.uuid == cls.menu_id)
            result = await db.execute(query)
            created_menu = result.scalar()
            assert created_menu.title == menu.json()["title"]
            assert created_menu.description == menu.json()["description"]

    @classmethod
    @pytest.mark.asyncio
    async def test_all_submenus_is_empty(cls, ac: AsyncClient):
        async with async_session_maker() as db:
            response = await ac.get(f"/api/v1/menus/{cls.menu_id}/submenus/")
            submenus_query = select(Submenu).where(Submenu.menu_id == cls.menu_id)
            submenus_result = await db.execute(submenus_query)
            submenus = submenus_result.fetchall()
            assert response.status_code == 200
            assert response.json() == []
            assert len(response.json()) == len(submenus)

    @classmethod
    @pytest.mark.asyncio
    async def test_post_submenu(cls, ac: AsyncClient):
        async with async_session_maker() as db:
            submenu = await ac.post(f'/api/v1/menus/{cls.menu_id}/submenus/', json={
                "title": "My submenu 1",
                "description": "My submenu description 1"
            })
            assert submenu.status_code == 201
            cls.submenu_id = submenu.json()["id"]
            query = select(Submenu).where(Submenu.uuid == cls.submenu_id)
            result = await db.execute(query)
            created_submenu = result.scalar()
            assert created_submenu.title == submenu.json()["title"]
            assert created_submenu.description == submenu.json()["description"]

    @classmethod
    @pytest.mark.asyncio
    async def test_get_submenu(cls, ac: AsyncClient):
        async with async_session_maker() as db:
            response = await ac.get(f'/api/v1/menus/{cls.menu_id}/submenus/{cls.submenu_id}')
            query = select(Submenu).where(Submenu.uuid == cls.submenu_id)
            result = await db.execute(query)
            submenu = result.scalar()
            assert response.json() != []
            assert response.json()['title'] == submenu.title
            assert response.json()['description'] == submenu.description
            assert response.status_code == 200

    @classmethod
    @pytest.mark.asyncio
    async def test_patch_submenu(cls, ac: AsyncClient):
        async with async_session_maker() as db:
            response = await ac.patch(f'/api/v1/menus/{cls.menu_id}/submenus/{cls.submenu_id}', json={
                "title": "My updated submenu 1",
                "description": "My updated submenu description 1"
            })
            assert response.status_code == 200
            query = select(Submenu).where(Submenu.uuid == cls.submenu_id)
            result = await db.execute(query)
            updated_submenu = result.scalar()
            assert updated_submenu.title == response.json()["title"]
            assert updated_submenu.description == response.json()["description"]
            assert response.json() != []
            assert response.json() == response.json()

    @classmethod
    @pytest.mark.asyncio
    async def test_delete_submenu(cls, ac: AsyncClient):
        async with async_session_maker() as db:
            response = await ac.delete(f'/api/v1/menus/{cls.menu_id}/submenus/{cls.submenu_id}')
            assert response.status_code == 200
            response = await ac.get(f'/api/v1/menus/{cls.menu_id}/submenus/{cls.submenu_id}')
            assert response.status_code == 404
            query = select(Submenu).where(Submenu.uuid == cls.submenu_id)
            result = await db.execute(query)
            deleted_submenu = result.scalar()
            assert deleted_submenu is None
            assert response.json()["detail"] == 'submenu not found'
