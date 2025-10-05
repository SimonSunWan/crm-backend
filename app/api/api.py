from fastapi import APIRouter

from app.api import auth, cache, department, dictionary, menu, order, role, system, user

api_router = APIRouter()

# 路由配置
ROUTES = [
    (auth.router, "/auth", ["auth"]),
    (user.router, "/users", ["users"]),
    (dictionary.router, "/dictionary", ["dictionary"]),
    (role.router, "/roles", ["roles"]),
    (menu.router, "/menus", ["menus"]),
    (department.router, "/departments", ["departments"]),
    (order.router, "/orders", ["orders"]),
    (system.router, "/system", ["system-settings"]),
    (cache.router, "/cache", ["cache"])
]

for router, prefix, tags in ROUTES:
    api_router.include_router(router, prefix=prefix, tags=tags)
