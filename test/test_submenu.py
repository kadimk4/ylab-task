import pytest
from httpx import AsyncClient

id_dict = {
    "menu_id": None,
    "submenu_id": None,

}

@pytest.mark.asyncio
async def test_all_submenus_is_empty(ac: AsyncClient):
    menu = await ac.post('/api/v1/menus/', json={
        "title": "My menu 1",
        "description": "My menu description 1"
    })
    assert menu.status_code == 201
    id_dict['menu_id'] = menu.json()["id"]
    menu_id = id_dict["menu_id"]
    res = await ac.get(f'/api/v1/menus/{menu_id}')
    assert res.json() == menu.json()
    assert res.status_code == 200

    response = await ac.get(f'/api/v1/menus/{menu_id}/submenus/')
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_post_submenu(ac: AsyncClient):
    menu_id = id_dict["menu_id"]
    response = await ac.post(f'/api/v1/menus/{menu_id}/submenus/', json={
        "title": "My submenu 1",
        "description": "My submenu description 1"
    })
    assert response.status_code == 201
    id_dict['submenu_id'] = response.json()['id']
    submenu_id = id_dict['submenu_id']
    res = await ac.get(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}')
    assert res.json() != []
    assert res.json() == response.json()
    assert res.status_code == 200



@pytest.mark.asyncio
async def test_get_submenu(ac: AsyncClient):
    menu_id, submenu_id = id_dict["menu_id"], id_dict["submenu_id"]
    response = await ac.get(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}')
    assert response.status_code == 200
    assert response.json() != []
    assert response.json()['title'] == "My submenu 1"
    assert response.json()['description'] == "My submenu description 1"



@pytest.mark.asyncio
async def test_patch_submenu(ac: AsyncClient):
    menu_id, submenu_id = id_dict["menu_id"], id_dict["submenu_id"]
    response = await ac.patch(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}', json={
        "title": "My updated submenu 1",
        "description": "My updated submenu description 1"
    })
    assert response.status_code == 200
    res = await ac.get(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}')
    assert res.status_code == 200
    assert res.json() != []
    assert res.json() == response.json()


@pytest.mark.asyncio
async def test_delete_submenu(ac: AsyncClient):
    menu_id, submenu_id = id_dict["menu_id"], id_dict["submenu_id"]
    response = await ac.delete(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}')
    assert response.status_code == 200
    response = await ac.get(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}')
    assert response.json()['detail'] == 'submenu not found'
    assert response.status_code == 404
    response = await ac.get(f'/api/v1/menus/{submenu_id}/submenus/')
    assert len(response.json()) == 0
