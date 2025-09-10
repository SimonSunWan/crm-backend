from fastapi import APIRouter, HTTPException

from app.core.redis_client import cache_manager, redis_client
from app.schemas.base import ApiResponse

router = APIRouter()


@router.get("/health", response_model=ApiResponse)
def health_check():
    """系统健康检查"""
    health_data = {
        "status": "healthy",
        "redis": "connected" if redis_client.is_connected() else "disconnected",
        "cache_enabled": redis_client.is_connected(),
    }

    return ApiResponse(data=health_data)


@router.get("/cache/stats", response_model=ApiResponse)
def cache_stats():
    """缓存统计信息"""
    if not redis_client.is_connected():
        raise HTTPException(status_code=503, detail="Redis未连接")

    try:
        redis_client_instance = redis_client.client
        info = redis_client_instance.info()

        stats = {
            "connected_clients": info.get("connected_clients", 0),
            "used_memory": info.get("used_memory_human", "0B"),
            "total_commands_processed": info.get("total_commands_processed", 0),
            "keyspace_hits": info.get("keyspace_hits", 0),
            "keyspace_misses": info.get("keyspace_misses", 0),
            "uptime_in_seconds": info.get("uptime_in_seconds", 0),
        }

        return ApiResponse(data=stats)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取缓存统计失败: {str(e)}")


@router.post("/cache/clear", response_model=ApiResponse)
def clear_cache():
    """清除所有缓存"""
    if not redis_client.is_connected():
        raise HTTPException(status_code=503, detail="Redis未连接")

    try:
        redis_client_instance = redis_client.client
        redis_client_instance.flushdb()

        return ApiResponse(message="缓存清除成功")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"清除缓存失败: {str(e)}")


@router.post("/cache/clear-pattern", response_model=ApiResponse)
def clear_cache_pattern(pattern: str):
    """按模式清除缓存"""
    if not redis_client.is_connected():
        raise HTTPException(status_code=503, detail="Redis未连接")

    try:
        deleted_count = cache_manager.delete_pattern(pattern)

        return ApiResponse(
            message="缓存清除成功",
            data={"pattern": pattern, "deleted_count": deleted_count},
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"清除缓存失败: {str(e)}")
