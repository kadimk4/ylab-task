from fastapi import FastAPI
from src.api.routers import menus, submenus, dishes


app = FastAPI()

app.include_router(menus.router)
app.include_router(submenus.router)
app.include_router(dishes.router)