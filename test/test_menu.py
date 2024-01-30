import pytest
from httpx import AsyncClient
from sqlalchemy import select

from models.menu import Menu
from conftest import async_session_maker


class TestMenus:
    menu_id = None

    @pytest.mark.asyncio
    async def test_all_menus_is_empty(self, ac: AsyncClient):
        async with async_session_maker() as db:
            response = await ac.get(f"/api/v1/menus/")
            menus_query = select(Menu)
            menus_result = await db.execute(menus_query)
            menus = menus_result.fetchall()
            assert response.status_code == 200
            assert response.json() == []
            assert len(response.json()) == len(menus)

    @classmethod
    @pytest.mark.asyncio
    async def test_post_menu(cls, ac: AsyncClient):
        async with async_session_maker() as db:
            response = await ac.post(f'/api/v1/menus/', json={
                "title": "My menu 1",
                "description": "My menu description 1",

            })
            assert response.status_code == 201
            query = select(Menu).where(Menu.uuid == response.json()["id"])
            result = await db.execute(query)
            created_menu = result.scalar()
            assert created_menu.title == response.json()["title"]
            assert created_menu.description == response.json()["description"]
            cls.menu_id = response.json()["id"]

    @classmethod
    @pytest.mark.asyncio
    async def test_get_menu(cls, ac: AsyncClient):
        async with async_session_maker() as db:
            response = await ac.get(f'/api/v1/menus/{cls.menu_id}')
            query = select(Menu).where(Menu.uuid == cls.menu_id)
            result = await db.execute(query)
            menu = result.scalar()
            assert response.json() != []
            assert response.json()['title'] == menu.title
            assert response.json()['description'] == menu.description
            assert response.status_code == 200

    @classmethod
    @pytest.mark.asyncio
    async def test_patch_menu(cls, ac: AsyncClient):
        async with async_session_maker() as db:
            response = await ac.patch(f'/api/v1/menus/{cls.menu_id}', json={
                "title": "My updated menu 1",
                "description": "My updated menu description 1"
            })
            assert response.status_code == 200
            query = select(Menu).where(Menu.uuid == cls.menu_id)
            result = await db.execute(query)
            updated_menu = result.scalar()
            assert updated_menu.title == response.json()["title"]
            assert updated_menu.description == response.json()["description"]
            assert response.json() != []
            assert response.json() == response.json()

    @classmethod
    @pytest.mark.asyncio
    async def test_delete_menu(cls, ac: AsyncClient):
        async with async_session_maker() as db:
            response = await ac.delete(f'/api/v1/menus/{cls.menu_id}')
            assert response.status_code == 200
            response = await ac.get(f'/api/v1/menus/{cls.menu_id}')
            assert response.status_code == 404
            query = select(Menu).where(Menu.uuid == cls.menu_id)
            result = await db.execute(query)
            deleted_menu = result.scalar()
            assert deleted_menu is None
            assert response.json()["detail"] == 'menu not found'
