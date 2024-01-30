import pytest
from httpx import AsyncClient

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.menu import Menu, Submenu, Dishes
from conftest import async_session_maker


class TestCase:
    menu_id = None
    submenu_id = None
    dish_id = None

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
    async def test_create_submenu(cls, ac: AsyncClient):
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
    async def test_all_dishes_is_empty(cls, ac: AsyncClient):
        async with async_session_maker() as db:
            response = await ac.get(f"/api/v1/menus/{cls.menu_id}/submenus/{cls.submenu_id}/dishes/")
            dishes_query = select(Dishes).where(Dishes.submenu_id == cls.submenu_id)
            dishes_result = await db.execute(dishes_query)
            dishes = dishes_result.fetchall()
            assert response.status_code == 200
            assert response.json() == []
            assert len(response.json()) == len(dishes)

    @classmethod
    @pytest.mark.asyncio
    async def test_post_dish(cls, ac: AsyncClient):
        async with async_session_maker() as db:
            response = await ac.post(f'/api/v1/menus/{cls.menu_id}/submenus/{cls.submenu_id}/dishes/', json={
                "title": "My dish 1",
                "description": "My dish description 1",
                "price": "12.50"
            })
            assert response.status_code == 201
            query = select(Dishes).where(Dishes.uuid == response.json()["id"])
            result = await db.execute(query)
            created_dish = result.scalar()
            assert created_dish.title == response.json()["title"]
            assert created_dish.description == response.json()["description"]
            assert created_dish.price == response.json()["price"]
            cls.dish_id = response.json()["id"]

    @classmethod
    @pytest.mark.asyncio
    async def test_get_dish(cls, ac: AsyncClient):
        async with async_session_maker() as db:
            response = await ac.get(f'/api/v1/menus/{cls.menu_id}/submenus/{cls.submenu_id}/dishes/{cls.dish_id}')
            query = select(Dishes).where(Dishes.uuid == cls.dish_id)
            result = await db.execute(query)
            dish = result.scalar()
            assert response.json() != []
            assert response.json()['title'] == dish.title
            assert response.json()['description'] == dish.description
            assert response.json()['price'] == dish.price
            assert response.status_code == 200

    @classmethod
    @pytest.mark.asyncio
    async def test_patch_dish(cls, ac: AsyncClient):
        async with async_session_maker() as db:
            response = await ac.patch(f'/api/v1/menus/{cls.menu_id}/submenus/{cls.submenu_id}/dishes/{cls.dish_id}', json={
                "title": "My updated dish 1",
                "description": "My updated dish description 1",
                "price": "14.50"
            })
            assert response.status_code == 200
            query = select(Dishes).where(Dishes.uuid == cls.dish_id)
            result = await db.execute(query)
            updated_dish = result.scalar()
            assert updated_dish.title == response.json()["title"]
            assert updated_dish.description == response.json()["description"]
            assert updated_dish.price == response.json()["price"]
            assert response.json() != []
            assert response.json() == response.json()

    @classmethod
    @pytest.mark.asyncio
    async def test_delete_dish(cls, ac: AsyncClient):
        async with async_session_maker() as db:
            response = await ac.delete(f'/api/v1/menus/{cls.menu_id}/submenus/{cls.submenu_id}/dishes/{cls.dish_id}')
            assert response.status_code == 200
            response = await ac.get(f'/api/v1/menus/{cls.menu_id}/submenus/{cls.submenu_id}/dishes/{cls.dish_id}')
            assert response.status_code == 404
            query = select(Dishes).where(Dishes.uuid == cls.dish_id)
            result = await db.execute(query)
            deleted_dish = result.scalar()
            assert deleted_dish is None
            assert response.json()["detail"] == 'dish not found'
