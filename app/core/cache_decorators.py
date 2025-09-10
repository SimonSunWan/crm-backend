"""缓存装饰器"""

import functools
import logging
from typing import Callable, Optional

from app.core.redis_client import cache_manager

logger = logging.getLogger(__name__)


def cached(
    key_func: Optional[Callable] = None,
    ttl: Optional[int] = None,
    prefix: str = "cache",
):
    """缓存装饰器，支持自定义键生成和TTL"""

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # 生成缓存键
            if key_func:
                cache_key = key_func(*args, **kwargs)
            else:
                # 默认使用函数名和参数生成键
                key_parts = [prefix, func.__name__]
                key_parts.extend(str(arg) for arg in args)
                key_parts.extend(f"{k}={v}" for k, v in sorted(kwargs.items()))
                cache_key = ":".join(key_parts)

            # 尝试从缓存获取
            cached_result = cache_manager.get(cache_key)
            if cached_result is not None:
                logger.debug(f"缓存命中: {cache_key}")
                return cached_result

            # 执行原函数
            result = func(*args, **kwargs)

            # 存储到缓存
            if result is not None:
                cache_manager.set(cache_key, result, ttl)
                logger.debug(f"缓存存储: {cache_key}")

            return result

        return wrapper

    return decorator


def cache_invalidate(key_pattern: str):
    """缓存失效装饰器，按模式清除缓存"""

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)

            # 清除缓存
            deleted_count = cache_manager.delete_pattern(key_pattern)
            if deleted_count > 0:
                logger.debug(f"缓存失效: {key_pattern}, 删除 {deleted_count} 个键")

            return result

        return wrapper

    return decorator


def cache_refresh(key_func: Callable, ttl: Optional[int] = None):
    """缓存刷新装饰器，先清除再重新缓存"""

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # 生成缓存键
            cache_key = key_func(*args, **kwargs)

            # 清除现有缓存
            cache_manager.delete(cache_key)

            # 执行函数
            result = func(*args, **kwargs)

            # 重新缓存
            if result is not None:
                cache_manager.set(cache_key, result, ttl)
                logger.debug(f"缓存刷新: {cache_key}")

            return result

        return wrapper

    return decorator


class CacheContext:
    """缓存上下文管理器"""

    def __init__(self, key: str, ttl: Optional[int] = None):
        self.key = key
        self.ttl = ttl
        self.cached_value = None

    def __enter__(self):
        self.cached_value = cache_manager.get(self.key)
        return self.cached_value

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None and self.cached_value is None:
            # 如果没有异常且没有缓存值，可以在这里设置缓存
            pass


def with_cache(key: str, ttl: Optional[int] = None):
    """缓存上下文管理器装饰器"""
    return CacheContext(key, ttl)
