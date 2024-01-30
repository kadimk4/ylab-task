import pytest
from httpx import AsyncClient
from sqlalchemy import select

from models.menu import Submenu, Menu, Dishes
from conftest import async_session_maker


@pytest.mark.asyncio
async def test_dish_submenu_count(ac: AsyncClient):
    async with async_session_maker() as db:
        menu = await ac.post('/api/v1/menus/', json={
            "title": "My menu 1",
            "description": "My menu description 1"
        })
        assert menu.status_code == 201
        menu_id = menu.json()['id']

        query = select(Menu).where(Menu.uuid == menu_id)
        result = await db.execute(query)
        created_menu = result.scalar()
        assert created_menu is not None
        assert created_menu.title == menu.json()['title']
        assert created_menu.description == menu.json()['description']

        submenu = await ac.post(f'/api/v1/menus/{menu_id}/submenus/', json={
            "title": "My submenu 1",
            "description": "Mu submenu description 2"
        })
        assert submenu.status_code == 201
        submenu_id = submenu.json()['id']
        query = select(Submenu).where(Submenu.uuid == submenu_id)
        result = await db.execute(query)
        created_submenu = result.scalar()
        assert created_submenu is not None
        assert created_submenu.title == submenu.json()['title']
        assert created_submenu.description == submenu.json()['description']

        dish_1 = await ac.post(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/', json={
            "title": "My dish 1",
            "description": "My dish description 1",
            "price": "12.50"
        })
        assert dish_1.status_code == 201
        dish1_id = dish_1.json()['id']

        dish_2 = await ac.post(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/', json={
            "title": "My dish 2",
            "description": "My dish description 2",
            "price": "13.50"
        })
        assert dish_2.status_code == 201
        dish2_id = dish_2.json()['id']


        query = select(Dishes)
        result = await db.execute(query)
        created_dishes = result.unique().scalars().all()

        assert len(created_dishes) == 2


        menu = await ac.get(f'/api/v1/menus/{menu_id}')
        assert menu.status_code == 200
        assert menu.json()['submenus_count'] == 1
        assert menu.json()['dishes_count'] == 2

        await ac.delete(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}')

        query = select(Submenu).where(Submenu.uuid == submenu_id)
        result = await db.execute(query)
        deleted_submenu = result.scalar()
        assert deleted_submenu is None

        submenus = await ac.get(f'/api/v1/menus/{menu_id}/submenus/')
        assert submenus.status_code == 200
        assert submenus.json() == []

        dishes = await ac.get(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/')
        assert dishes.status_code == 200
        assert dishes.json() == []

        await ac.delete(f'/api/v1/menus/{menu_id}')

        query = select(Menu).where(Menu.uuid == menu_id)
        result = await db.execute(query)
        deleted_menu = result.scalar()
        assert deleted_menu is None

        menus = await ac.get('/api/v1/menus/')
        assert menus.status_code == 200
        assert menus.json() == []