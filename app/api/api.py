from fastapi import APIRouter

from app.api import auth, cache, dictionary, menu, order, role, system, user

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(user.router, prefix="/users", tags=["users"])
api_router.include_router(dictionary.router, prefix="/dictionary", tags=["dictionary"])
api_router.include_router(role.router, prefix="/roles", tags=["roles"])
api_router.include_router(menu.router, prefix="/menus", tags=["menus"])
api_router.include_router(order.router, prefix="/orders", tags=["orders"])
api_router.include_router(system.router, prefix="/system", tags=["system-settings"])
api_router.include_router(cache.router, prefix="/cache", tags=["cache"])
