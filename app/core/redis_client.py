"""
Redis客户端和缓存工具
提供统一的Redis连接和缓存操作接口
"""

import json
import logging
from typing import Any, Optional

import redis
from redis.connection import ConnectionPool

from app.core.config import settings

logger = logging.getLogger(__name__)


class RedisClient:
    """Redis客户端单例类"""

    _instance = None
    _redis_client = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if self._redis_client is None:
            self._init_redis_client()

    def _init_redis_client(self):
        """初始化Redis客户端"""
        # 直接禁用Redis连接
        self._redis_client = None

    @property
    def client(self) -> Optional[redis.Redis]:
        """获取Redis客户端"""
        return self._redis_client

    def is_connected(self) -> bool:
        """检查Redis是否连接"""
        if self._redis_client is None:
            return False
        try:
            self._redis_client.ping()
            return True
        except Exception:
            return False


# 全局Redis客户端实例
redis_client = RedisClient()


class CacheManager:
    """缓存管理器"""

    def __init__(self):
        self.redis = redis_client.client

    def _serialize(self, value: Any) -> str:
        """序列化数据"""
        if isinstance(value, str):
            return value
        return json.dumps(value, ensure_ascii=False)

    def _deserialize(self, value: str) -> Any:
        """反序列化数据"""
        try:
            return json.loads(value)
        except (json.JSONDecodeError, TypeError):
            return value

    def get(self, key: str) -> Optional[Any]:
        """获取缓存"""
        if not self.redis:
            return None

        try:
            value = self.redis.get(key)
            if value is not None:
                return self._deserialize(value)
            return None
        except Exception as e:
            logger.error(f"获取缓存失败 {key}: {e}")
            return None

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """设置缓存"""
        if not self.redis:
            return False

        try:
            serialized_value = self._serialize(value)
            if ttl is None:
                ttl = settings.CACHE_DEFAULT_TTL

            self.redis.setex(key, ttl, serialized_value)
            return True
        except Exception as e:
            logger.error(f"设置缓存失败 {key}: {e}")
            return False

    def delete(self, key: str) -> bool:
        """删除缓存"""
        if not self.redis:
            return False

        try:
            self.redis.delete(key)
            return True
        except Exception as e:
            logger.error(f"删除缓存失败 {key}: {e}")
            return False

    def delete_pattern(self, pattern: str) -> int:
        """按模式删除缓存"""
        if not self.redis:
            return 0

        try:
            keys = self.redis.keys(pattern)
            if keys:
                return self.redis.delete(*keys)
            return 0
        except Exception as e:
            logger.error(f"按模式删除缓存失败 {pattern}: {e}")
            return 0

    def exists(self, key: str) -> bool:
        """检查缓存是否存在"""
        if not self.redis:
            return False

        try:
            return bool(self.redis.exists(key))
        except Exception as e:
            logger.error(f"检查缓存存在失败 {key}: {e}")
            return False

    def expire(self, key: str, ttl: int) -> bool:
        """设置缓存过期时间"""
        if not self.redis:
            return False

        try:
            return bool(self.redis.expire(key, ttl))
        except Exception as e:
            logger.error(f"设置缓存过期时间失败 {key}: {e}")
            return False

    def get_ttl(self, key: str) -> int:
        """获取缓存剩余时间"""
        if not self.redis:
            return -1

        try:
            return self.redis.ttl(key)
        except Exception as e:
            logger.error(f"获取缓存TTL失败 {key}: {e}")
            return -1


# 全局缓存管理器实例
cache_manager = CacheManager()


def get_cache_key(prefix: str, *args) -> str:
    """生成缓存键"""
    return f"{prefix}:{':'.join(str(arg) for arg in args)}"


def cache_key_user(user_id: int) -> str:
    """用户缓存键"""
    return get_cache_key("user", user_id)


def cache_key_user_by_username(username: str) -> str:
    """用户名缓存键"""
    return get_cache_key("user:username", username)


def cache_key_user_by_email(email: str) -> str:
    """用户邮箱缓存键"""
    return get_cache_key("user:email", email)


def cache_key_menu_tree() -> str:
    """菜单树缓存键"""
    return "menu:tree"


def cache_key_menu_by_id(menu_id: int) -> str:
    """菜单缓存键"""
    return get_cache_key("menu", menu_id)


def cache_key_dictionary_by_code(code: str) -> str:
    """字典缓存键"""
    return get_cache_key("dictionary", code)


def cache_key_role_by_id(role_id: int) -> str:
    """角色缓存键"""
    return get_cache_key("role", role_id)


def cache_key_role_by_code(role_code: str) -> str:
    """角色编码缓存键"""
    return get_cache_key("role:code", role_code)
