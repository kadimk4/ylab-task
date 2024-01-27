import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.menu import Dishes, Submenu, Menu


class DishCrud:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self) -> list[dict[str, str]]:
        req = await self.db.execute(select(Dishes))
        dishes = req.unique().scalars().all()
        dishes_list = [
            {
                'id': str(dish.uuid),
                'submenu_id': str(dish.submenu_id),
                'title': dish.title,
                'description': dish.description,
                'price': dish.price
            }
            for dish in dishes
        ]
        return dishes_list

    async def get(self, uuid_str: uuid = None) -> dict[str, str]:
        dish = await self.db.get(Dishes, uuid_str)
        if dish:
            return {
                'id': str(dish.uuid),
                'submenu_id': str(dish.submenu_id),
                'title': dish.title,
                'description': dish.description,
                'price': dish.price
            }

    async def post(self, submenu_str: uuid = None, title: str = None, desc: str = None, price: str = None) -> dict[
        str, str]:
        dish = Dishes(title=title, description=desc, submenu_id=submenu_str, price=price)
        self.db.add(dish)
        await self.db.commit()
        await self.db.refresh(dish)
        return {
            'id': str(dish.uuid),
            'submenu_id': str(dish.submenu_id),
            'title': dish.title,
            'description': dish.description,
            'price': dish.price
        }

    async def patch(self, submenu_str: uuid, uuid_str: uuid = None, title: str = None, desc: str = None,
                    price: str = None) -> dict[str, str]:
        dish = await self.db.get(Dishes, uuid_str)
        if dish:
            dish.title = title
            dish.description = desc
            dish.submenu_id = submenu_str
            dish.price = price
            await self.db.commit()
            await self.db.refresh(dish)
            return {
                'id': str(dish.uuid),
                'submenu_id': str(dish.submenu_id),
                'title': dish.title,
                'description': dish.description,
                'price': dish.price
            }

    async def delete(self, uuid_str: uuid = None) -> dict[str, str] | None:
        dish = await self.db.get(Dishes, uuid_str)
        if dish:
            await self.db.delete(dish)
            await self.db.commit()
            return {
                'id': str(dish.uuid),
                'submenu_id': str(dish.submenu_id),
                'title': dish.title,
                'description': dish.description,
                'price': dish.price
            }


class SubmenuCrud:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, uuid_str: uuid = None) -> dict[str, str] | None:
        submenu = await self.db.get(Submenu, uuid_str)
        if submenu:
            return {
                'id': str(submenu.uuid),
                'title': submenu.title,
                'description': submenu.description,
                'menu_id': str(submenu.menu_id),
                'dishes_count': len(submenu.dishes)
            }

    async def get_all(self) -> list[dict[str, str]]:
        res = await self.db.execute(select(Submenu))
        submenus = res.unique().scalars().all()
        submenus_list = [
            {
                'id': str(submenu.uuid),
                'menu_id': str(submenu.menu_id),
                'title': submenu.title,
                'description': submenu.description,
                'dishes': [
                    {
                        'id': str(dish.uuid),
                        'submenu_id': str(dish.submenu_id),
                        'title': dish.title,
                        'description': dish.description,
                        'price': dish.price
                    }
                    for dish in submenu.dishes
                ]
            }
            for submenu in submenus
        ]
        return submenus_list

    async def patch(self, menu_id: uuid, uuid_str: uuid = None, title: str = None, desc: str = None) -> dict[str, str]:
        submenu = await self.db.get(Submenu, uuid_str)
        if submenu:
            submenu.title = title
            submenu.description = desc
            submenu.menu_id = menu_id
            await self.db.commit()
            await self.db.refresh(submenu)
            return {
                'id': str(submenu.uuid),
                'title': submenu.title,
                'description': submenu.description,
                'menu_id': str(submenu.menu_id),
                'dishes_count': len(submenu.dishes)
            }

    async def post(self, title: str = None, desc: str = None, menu_id: uuid = None) -> dict[str, str]:
        submenu = Submenu(title=title, description=desc, menu_id=menu_id)
        self.db.add(submenu)
        await self.db.commit()
        await self.db.refresh(submenu)
        return {
            'id': str(submenu.uuid),
            'title': submenu.title,
            'description': submenu.description,
            'menu_id': str(submenu.menu_id),
            'dishes_count': len(submenu.dishes)
        }

    async def delete(self, uuid_str: uuid = None) -> dict[str, str] | None:
        submenu = await self.db.get(Submenu, uuid_str)
        if submenu:
            await self.db.delete(submenu)
            await self.db.commit()
            return {
                'id': str(submenu.uuid),
                'title': submenu.title,
                'description': submenu.description,
                'menu_id': str(submenu.menu_id),
                'dishes_count': len(submenu.dishes)
            }


class MenuCrud:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, uuid_str: uuid = None) -> dict[str, str] | None:
        menu = await self.db.get(Menu, uuid_str)
        if menu:
            return {
                'id': str(menu.uuid),
                'title': menu.title,
                'description': menu.description,
                'submenus_count': len(menu.submenus),
                'dishes_count': sum(len(submenu.dishes) for submenu in menu.submenus)
            }

    async def patch(self, uuid_str: uuid = None, title: str = None, desc: str = None) -> dict[str, str] | None:
        menu = await self.db.get(Menu, uuid_str)
        if menu:
            menu.title = title
            menu.description = desc
            await self.db.commit()
            await self.db.refresh(menu)
            return {
                'id': str(menu.uuid),
                'title': menu.title,
                'description': menu.description,
                'submenus_count': len(menu.submenus),
                'dishes_count': sum(len(submenu.dishes) for submenu in menu.submenus)
            }

    async def get_all(self) -> list[dict[str, str]]:
        res = await self.db.execute(select(Menu))
        menus = res.unique().scalars().all()
        menus_list = [
            {
                'id': str(menu.uuid),
                'title': menu.title,
                'description': menu.description,
                'submenus': [
                    {
                        'id': str(submenu.uuid),
                        'menu_id': str(submenu.menu_id),
                        'title': submenu.title,
                        'description': submenu.description,
                        'dishes': [
                            {
                                'id': str(dish.uuid),
                                'submenu_id': str(dish.submenu_id),
                                'title': dish.title,
                                'description': dish.description,
                                'price': dish.price
                            }
                            for dish in submenu.dishes
                        ]
                    }
                    for submenu in menu.submenus
                ]
            }
            for menu in menus
        ]
        return menus_list

    async def delete(self, uuid_str: uuid = None) -> dict[str, str] | None:
        menu = await self.db.get(Menu, uuid_str)
        if menu:
            await self.db.delete(menu)
            await self.db.commit()
            return {
                'id': str(menu.uuid),
                'title': menu.title,
                'description': menu.description,
                'submenus_count': len(menu.submenus),
                'dishes_count': sum(len(submenu.dishes) for submenu in menu.submenus)
            }

    async def post(self, title: str = None, desc: str = None) -> dict[str, str]:
        menu = Menu(title=title, description=desc)
        self.db.add(menu)
        await self.db.commit()
        await self.db.refresh(menu)
        return {
            'id': str(menu.uuid),
            'title': menu.title,
            'description': menu.description,
            'submenus_count': len(menu.submenus),
            'dishes_count': sum(len(submenu.dishes) for submenu in menu.submenus)
        }
