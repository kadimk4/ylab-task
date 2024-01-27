import pytest
from httpx import AsyncClient

id_dict = {
    "menu_id": None,
    "submenu_id": None,
    "dish_id": None
}


@pytest.mark.asyncio
async def test_all_dishes_is_empty(ac: AsyncClient):
    menu = await ac.post('/api/v1/menus/', json={
        "title": "My menu 1",
        "description": "My menu description 1"
    })
    assert menu.status_code == 201
    menu_id = menu.json()["id"]
    res = await ac.get(f'/api/v1/menus/{menu_id}')
    assert menu.json() == res.json()
    assert res.status_code == 200

    submenu = await ac.post(f'/api/v1/menus/{menu_id}/submenus/', json={
        "title": "My submenu 1",
        "description": "My submenu description 1"
    })
    assert submenu.status_code == 201
    submenu_id = submenu.json()["id"]
    res = await ac.get(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}')
    assert res.json() == submenu.json()
    assert res.status_code == 200

    response = await ac.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/")
    assert response.status_code == 200
    assert response.json() == []
    id_dict['menu_id'], id_dict['submenu_id'] = menu_id, submenu_id


@pytest.mark.asyncio
async def test_post_dish(ac: AsyncClient):
    menu_id, submenu_id = id_dict["menu_id"], id_dict["submenu_id"]
    response = await ac.post(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/', json={
        "title": "My dish 1",
        "description": "My dish description 1",
        "price": "12.50"
    })
    assert response.status_code == 201
    dish_id = response.json()["id"]
    id_dict["dish_id"] = dish_id
    res = await ac.get(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
    assert res.status_code == 200
    assert res.json() != []
    assert res.json() == response.json()


@pytest.mark.asyncio
async def test_get_dish(ac: AsyncClient):
    menu_id, submenu_id, dish_id = id_dict["menu_id"], id_dict["submenu_id"], id_dict["dish_id"]
    response = await ac.get(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
    assert response.json() != []
    assert response.json()['title'] == 'My dish 1'
    assert response.json()['description'] == 'My dish description 1'
    assert response.json()['price'] == '12.50'
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_patch_dish(ac: AsyncClient):
    menu_id, submenu_id, dish_id = id_dict["menu_id"], id_dict["submenu_id"], id_dict["dish_id"]
    response = await ac.patch(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}', json={
        "title": "My updated dish 1",
        "description": "My updated dish description 1",
        "price": "14.50"
    })
    assert response.status_code == 200
    res = await ac.get(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
    assert res.status_code == 200
    assert res.json() != []
    assert res.json() == response.json()



@pytest.mark.asyncio
async def test_delete_dish(ac: AsyncClient):
    menu_id, submenu_id, dish_id = id_dict["menu_id"], id_dict["submenu_id"], id_dict["dish_id"]
    response = await ac.delete(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
    assert response.status_code == 200
    response = await ac.get(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
    assert response.json()["detail"] == "dish not found"
    assert response.status_code == 404
    response = await ac.get(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/')
    assert response.json() == []
