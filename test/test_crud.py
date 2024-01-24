from httpx import AsyncClient
import pytest


# CRUD FOR MENU
@pytest.mark.asyncio
async def test_all_menus_is_empty(ac: AsyncClient):
    response = await ac.get('/api/v1/menus/')
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_post_menu(ac: AsyncClient):
    global menu_id
    response = await ac.post('/api/v1/menus/', json={
        "title": "My menu 1",
        "description": "My menu description 1"
    })
    assert response.status_code == 201
    menu_id = response.json()['id']
    response = await ac.get('/api/v1/menus/')
    assert len(response.json()) == 1


@pytest.mark.asyncio
async def test_get_menu(ac: AsyncClient):
    global menu_id
    response = await ac.get(f'/api/v1/menus/{menu_id}')
    assert response.status_code == 200
    assert response.json()['title'] == "My menu 1"
    assert response.json()['description'] == "My menu description 1"


@pytest.mark.asyncio
async def test_patch_menu(ac: AsyncClient):
    global menu_id
    response = await ac.patch(f'/api/v1/menus/{menu_id}', json={
        "title": "My updated menu 1",
        "description": "My updated menu description 1"
    })
    assert response.status_code == 200
    assert response.json()['title'] == "My updated menu 1"
    assert response.json()['description'] == "My updated menu description 1"

# CRUD FOR SUBMENU


@pytest.mark.asyncio
async def test_all_submenus_is_empty(ac: AsyncClient):
    global menu_id
    response = await ac.get(f'/api/v1/menus/{menu_id}/submenus/')
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_post_submenu(ac: AsyncClient):
    global menu_id
    global submenu_id
    response = await ac.post(f'/api/v1/menus/{menu_id}/submenus/', json={
        "title": "My submenu 1",
        "description": "My submenu description 1"
    })
    assert response.status_code == 201
    submenu_id = response.json()['id']
    response = await ac.get(f'/api/v1/menus/{menu_id}/submenus/')
    assert len(response.json()) == 1


@pytest.mark.asyncio
async def test_get_submenu(ac: AsyncClient):
    global menu_id
    global submenu_id
    response = await ac.get(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}')
    assert response.status_code == 200
    assert response.json()['title'] == "My submenu 1"
    assert response.json()['description'] == "My submenu description 1"


@pytest.mark.asyncio
async def test_patch_submenu(ac: AsyncClient):
    global menu_id
    global submenu_id
    response = await ac.patch(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}', json={
        "title": "My updated submenu 1",
        "description": "My updated submenu description 1"
    })
    assert response.status_code == 200
    assert response.json()['title'] == "My updated submenu 1"
    assert response.json()['description'] == "My updated submenu description 1"


# CRUD FOR DISHES


@pytest.mark.asyncio
async def test_all_dishes_is_empty(ac: AsyncClient):
    global menu_id
    global submenu_id
    response = await ac.get(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/')
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_post_dish(ac: AsyncClient):
    global menu_id
    global submenu_id
    global dish_id
    response = await ac.post(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/', json={
        "title": "My dish 1",
        "description": "My dish description 1",
        "price": "12.50"
    })
    assert response.status_code == 201
    dish_id = response.json()['id']
    print(dish_id)
    response = await ac.get(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/')
    assert len(response.json()) == 1


@pytest.mark.asyncio
async def test_get_dish(ac: AsyncClient):
    global menu_id
    global submenu_id
    global dish_id
    response = await ac.get(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
    assert response.status_code == 200
    assert response.json()['title'] == "My dish 1"
    assert response.json()['description'] == "My dish description 1"
    assert response.json()['price'] == "12.50"


@pytest.mark.asyncio
async def test_patch_dish(ac: AsyncClient):
    global menu_id
    global submenu_id
    global dish_id
    response = await ac.patch(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}', json={
        "title": "My updated dish 1",
        "description": "My updated dish description 1",
        "price": "14.50"
    })
    assert response.status_code == 200
    assert response.json()['title'] == "My updated dish 1"
    assert response.json()['description'] == "My updated dish description 1"
    assert response.json()['price'] == "14.50"

@pytest.mark.asyncio
async def test_delete_submenu(ac: AsyncClient):
    global menu_id
    global submenu_id
    response = await ac.delete(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}')
    assert response.status_code == 200
    response = await ac.get(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}')
    assert response.status_code == 404
    response = await ac.get(f'/api/v1/menus/{submenu_id}/submenus/')
    assert len(response.json()) == 0


@pytest.mark.asyncio
async def test_delete_menu(ac: AsyncClient):
    global menu_id
    response = await ac.delete(f'/api/v1/menus/{menu_id}')
    assert response.status_code == 200
    response = await ac.get(f'/api/v1/menus/{menu_id}')
    assert response.status_code == 404
    response = await ac.get('/api/v1/menus/')
    assert len(response.json()) == 0


