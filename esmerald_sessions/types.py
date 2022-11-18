from typing import Union

from esmerald_sessions.backends import (
    AioMemCacheSessionBackend,
    AioRedisSessionBackend,
    MemCacheSessionBackend,
    RedisSessionBackend,
)

PredefinedBackendType = Union[
    AioMemCacheSessionBackend, AioRedisSessionBackend, MemCacheSessionBackend, RedisSessionBackend
]
