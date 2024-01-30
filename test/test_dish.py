import pytest
from httpx import AsyncClient
from sqlalchemy import select
from models.menu import Dishes
from conftest import async_session_maker


@pytest.mark.asyncio
async def test_dish_crud(ac: AsyncClient, dish_id_fixture):
    menu, submenu, dish = dish_id_fixture
    menu_id, submenu_id, dish_id = menu.uuid, submenu.uuid, dish.uuid
    response = await ac.get(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/')
    assert response.status_code == 200
    assert len(response.json()) == 1

    response = await ac.get(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
    assert response.status_code == 200
    assert response.json()['id'] == str(dish_id)
    assert response.json()['title'] == "My dish 1"
    assert response.json()['description'] == "My dish description 1"
    assert response.json()['price'] == "12.50"

    updated_title = "My updated dish 1"
    updated_desc = "My updated dish 1 description"
    updated_price = "13.50"
    response = await ac.patch(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
                              json={"title": updated_title, "description": updated_desc, "price": updated_price})
    assert response.status_code == 200
    assert response.json()['title'] == updated_title
    assert response.json()['description'] == updated_desc
    assert response.json()['price'] == updated_price

    async with async_session_maker() as db:
        dish = await db.execute(select(Dishes).filter(Dishes.uuid == dish_id))
        dish_data = dish.scalar()
        assert dish_data.title == updated_title
        assert dish_data.description == updated_desc
        assert dish_data.price == updated_price

    response = await ac.delete(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
    assert response.status_code == 200
    assert response.json()['id'] == str(dish_id)
    assert response.json()['title'] == updated_title
    assert response.json()['description'] == updated_desc
    assert response.json()['price'] == updated_price

    async with async_session_maker() as db:
        dish = await db.execute(select(Dishes).filter(Dishes.uuid == dish_id))
        assert dish.scalar() is None


@pytest.mark.asyncio
async def test_dish_post(ac: AsyncClient, dish_id_fixture):
    menu, submenu, dish = dish_id_fixture
    menu_id, submenu_id, dish_id = menu.uuid, submenu.uuid, dish.uuid
    new_title = "My dish 1"
    new_desc = "My dish 1 Description"
    new_price = "12.50"
    response = await ac.post(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/',
                             json={"title": new_title, "description": new_desc, "price": new_price})
    assert response.status_code == 201
    assert response.json()['title'] == new_title
    assert response.json()['description'] == new_desc
    assert response.json()['price'] == new_price

    async with async_session_maker() as db:
        dish = await db.execute(select(Dishes).filter(Dishes.title == new_title))
        assert dish.scalar() is not None
