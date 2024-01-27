import pytest
from httpx import AsyncClient


id_dict = {
    'menu_id': None
}

@pytest.mark.asyncio
async def test_all_menus_is_empty(ac: AsyncClient):
    response = await ac.get('/api/v1/menus/')
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_post_menu(ac: AsyncClient):
    response = await ac.post(f'/api/v1/menus/', json={
        "title": "My menu 1",
        "description": "My menu description 1"
    })
    assert response.status_code == 201
    id_dict["menu_id"] = response.json()['id']
    menu_id = id_dict['menu_id']
    res = await ac.get(f'/api/v1/menus/{menu_id}')
    assert res.status_code == 200
    assert res.json() != []
    assert res.json() == response.json()


@pytest.mark.asyncio
async def test_get_menu(ac: AsyncClient):
    menu_id = id_dict["menu_id"]
    response = await ac.get(f'/api/v1/menus/{menu_id}')
    assert response.status_code == 200
    assert response.json() != []
    assert response.json()['title'] == "My menu 1"
    assert response.json()['description'] == "My menu description 1"

@pytest.mark.asyncio
async def test_patch_menu(ac: AsyncClient):
    menu_id = id_dict["menu_id"]
    response = await ac.patch(f'/api/v1/menus/{menu_id}', json={
        "title": "My updated menu 1",
        "description": "My updated menu description 1"
    })
    assert response.status_code == 200
    res = await ac.get(f'/api/v1/menus/{menu_id}')
    assert res.status_code == 200
    assert res.json() != []
    assert res.json() == response.json()



@pytest.mark.asyncio
async def test_delete_menu(ac: AsyncClient):
    menu_id = id_dict["menu_id"]
    response = await ac.delete(f'/api/v1/menus/{menu_id}')
    assert response.status_code == 200
    response = await ac.get(f'/api/v1/menus/{menu_id}')
    assert response.status_code == 404
    response = await ac.get(f'/api/v1/menus/')
    assert len(response.json()) == 0
