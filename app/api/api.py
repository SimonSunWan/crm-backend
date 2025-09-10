from fastapi import APIRouter
from app.api import users, auth, dictionary, roles, menus, orders, system_settings

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(dictionary.router, prefix="/dictionary", tags=["dictionary"])
api_router.include_router(roles.router, prefix="/roles", tags=["roles"])
api_router.include_router(menus.router, prefix="/menus", tags=["menus"])
api_router.include_router(orders.router, prefix="/orders", tags=["orders"])
api_router.include_router(system_settings.router, prefix="/system", tags=["system-settings"])
