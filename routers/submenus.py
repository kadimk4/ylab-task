import uuid
from typing import Optional

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from models.db import get_async_db
from schemas.schemas import SubmenuCreate
from services.crud import SubmenuCrud

router = APIRouter(prefix='/api/v1/menus/{menu_id}/submenus', tags=['Submenus'])


@router.get("/{uuid_str}")
async def get(uuid_str: Optional[uuid.UUID] | None, db: AsyncSession = Depends(get_async_db)) -> JSONResponse:
    response = SubmenuCrud(db)
    res = await response.get(uuid_str)
    if not res:
        return JSONResponse(content={'detail': 'submenu not found'}, status_code=status.HTTP_404_NOT_FOUND)
    return JSONResponse(content=res, status_code=status.HTTP_200_OK)


@router.get('/')
async def get_all(db: AsyncSession = Depends(get_async_db)) -> JSONResponse:
    response = SubmenuCrud(db)
    return JSONResponse(content=await response.get_all(), status_code=status.HTTP_200_OK)


@router.post('/')
async def post(item: SubmenuCreate | None, menu_id: Optional[uuid.UUID] | None,
               db: AsyncSession = Depends(get_async_db)) -> JSONResponse:
    response = SubmenuCrud(db)
    return JSONResponse(content=await response.post(item.title, item.description, menu_id),
                        status_code=status.HTTP_201_CREATED)


@router.patch('/{uuid_str}')
async def patch(menu_id: Optional[uuid.UUID], uuid_str: Optional[uuid.UUID] | None, item: SubmenuCreate | None,
                db: AsyncSession = Depends(get_async_db)) -> JSONResponse:
    response = SubmenuCrud(db)
    return JSONResponse(content=await response.patch(menu_id, uuid_str, item.title, item.description),
                        status_code=status.HTTP_200_OK)


@router.delete('/{uuid_str}')
async def delete(uuid_str: Optional[uuid.UUID] | None, db: AsyncSession = Depends(get_async_db)) -> JSONResponse:
    response = SubmenuCrud(db)
    return JSONResponse(content=await response.delete(uuid_str), status_code=status.HTTP_200_OK)
