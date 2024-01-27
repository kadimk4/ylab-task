import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_dish_submenu_count(ac: AsyncClient):
    menu = await ac.post(f'/api/v1/menus/', json={
        "title": "My meny 1",
        "description": "My menu description 1"
    })
    menu_id = menu.json()['id']
    res = await ac.get(f'/api/v1/menus/{menu_id}')
    assert res.json() == menu.json()
    assert menu.status_code == 201
    # создали и проверили меню в бд
    submenu = await ac.post(f'/api/v1/menus/{menu_id}/submenus/', json={
        "title": "My submenu 1",
        "description": "Mu submenu description 2"
    })
    submenu_id = submenu.json()['id']
    res = await ac.get(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}')
    assert res.json() == submenu.json()
    assert submenu.status_code == 201
    # создали и проверили подменю в бд
    dish_1 = await ac.post(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/', json={
        "title": "My dish 1",
        "description": "My dish description 1",
        "price": "12.50"
    })
    dish1_id = dish_1.json()['id']
    res = await ac.get(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish1_id}')
    assert res.json() == dish_1.json()
    assert dish_1.status_code == 201
    dish_2 = await ac.post(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/', json={
        "title": "My dish 2",
        "description": "My dish description 2",
        "price": "13.50"
    })
    dish2_id = dish_2.json()['id']
    res = await ac.get(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish2_id}')
    assert res.json() == dish_2.json()
    assert dish_2.status_code == 201
    # создали и проверили два блюда
    # проверяем кол-во блюд и подменю у

    menu = await ac.get(f'/api/v1/menus/{menu_id}')
    assert menu.status_code == 200
    assert menu.json()['submenus_count'] == 1
    assert menu.json()['dishes_count'] == 2

    await ac.delete(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}')
    submenus = await ac.get(f'/api/v1/menus/{menu_id}/submenus/')
    assert submenus.json() == []
    assert submenus.status_code == 200


    dishes = await ac.get(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/')
    assert dishes.json() == []
    assert dishes.status_code == 200

    await ac.delete(f'/api/v1/menus/{menu_id}')
    menus = await ac.get(f'/api/v1/menus/')
    assert menus.json() == []
    assert menus.status_code == 200