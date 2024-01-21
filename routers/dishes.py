from typing import Optional

from fastapi import APIRouter, Depends
import uuid

from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.responses import JSONResponse

from models.db import get_async_db
from schemas.menu import DishCreate
from services.crud import DishCrud

router = APIRouter(prefix='/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes', tags=['Dishes'])


@router.get("/{uuid_str}")
async def get(uuid_str: Optional[uuid.UUID] | None, db: AsyncSession = Depends(get_async_db)) -> JSONResponse:
    response = DishCrud(db)
    res = await response.get(uuid_str)
    if not res:
        return JSONResponse(content={'detail': 'dish not found'}, status_code=status.HTTP_404_NOT_FOUND)
    return JSONResponse(content=res, status_code=status.HTTP_200_OK)


@router.get('/')
async def get_all(db: AsyncSession = Depends(get_async_db)) -> JSONResponse:
    response = DishCrud(db)
    return JSONResponse(content=await response.get_all(), status_code=status.HTTP_200_OK)


@router.post('/')
async def post(submenu_id: Optional[uuid.UUID] | None, item: DishCreate | None,
               db: AsyncSession = Depends(get_async_db)) -> JSONResponse:
    response = DishCrud(db)
    return JSONResponse(content=await response.post(submenu_id, item.title, item.description, item.price),
                        status_code=status.HTTP_201_CREATED)


@router.patch('/{uuid_str}')
async def patch(submenu_id: Optional[uuid.UUID], uuid_str: Optional[uuid.UUID] | None, item: DishCreate | None,
                db: AsyncSession = Depends(get_async_db)) -> JSONResponse:
    response = DishCrud(db)
    return JSONResponse(content=await response.patch(submenu_id, uuid_str, item.title, item.description, item.price),
                        status_code=status.HTTP_200_OK)


@router.delete('/{uuid_str}')
async def delete(uuid_str: Optional[uuid.UUID] | None, db: AsyncSession = Depends(get_async_db)) -> JSONResponse:
    response = DishCrud(db)
    return JSONResponse(content=await response.delete(uuid_str), status_code=status.HTTP_200_OK)
