import uuid
from typing import Optional

from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from models.db import get_async_db
from schemas.schemas import MenuCreate
from services.crud import MenuCrud

router = APIRouter(prefix='/api/v1/menus', tags=['Menus'])


@router.get('/{uuid_str}')
async def get_menu(uuid_str: Optional[uuid.UUID] | None, db: AsyncSession = Depends(get_async_db)) -> JSONResponse:
    response = MenuCrud(db)
    res = await response.get(uuid_str)
    if not res:
        return JSONResponse(content={'detail': 'menu not found'}, status_code=status.HTTP_404_NOT_FOUND)
    return JSONResponse(content=res, status_code=status.HTTP_200_OK)


@router.get("/")
async def get_all_menu(db: AsyncSession = Depends(get_async_db)) -> JSONResponse:
    model = MenuCrud(db)
    response = await model.get_all()
    return JSONResponse(content=response, status_code=status.HTTP_200_OK)


@router.post('/')
async def post_menu(item: MenuCreate | None, db: AsyncSession = Depends(get_async_db)) -> JSONResponse:
    response = MenuCrud(db)
    return JSONResponse(content=await response.post(item.title, item.description), status_code=status.HTTP_201_CREATED)


@router.patch("/{uuid_str}")
async def patch_menu(uuid_str: Optional[uuid.UUID] | None, item: MenuCreate | None,
                     db: AsyncSession = Depends(get_async_db)) -> JSONResponse:
    response = MenuCrud(db)
    res = await response.patch(uuid_str, item.title, item.description)
    if response:
        return JSONResponse(content=res, status_code=status.HTTP_200_OK)
    return JSONResponse(content={'detail': 'menu not found'}, status_code=status.HTTP_404_NOT_FOUND)


@router.delete('/{uuid_str}')
async def delete_menu(uuid_str: Optional[uuid.UUID] | None, db: AsyncSession = Depends(get_async_db)) -> JSONResponse:
    response = MenuCrud(db)
    return JSONResponse(content=await response.delete(uuid_str), status_code=status.HTTP_200_OK)
