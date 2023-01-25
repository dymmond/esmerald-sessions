from typing import TYPE_CHECKING, Any, Optional, Union

import orjson
from aiomcache import Client as AioMemcache
from aioredis import Redis as AioRedis
from pymemcache.client.base import Client as MemCache
from redis import Redis

from esmerald_sessions.datastructures import MemCacheJSONSerde
from esmerald_sessions.protocols import SessionBackend

if TYPE_CHECKING:
    from pydantic.typing import DictAny


class RedisSessionBackend(SessionBackend):
    """
    Backend for redis.
    """

    redis: Optional[Redis]

    def __init__(self, redis: Redis, **kwargs) -> None:
        super().__init__(**kwargs)
        self.redis = redis

    async def get(self, key: str, **kwargs: "DictAny") -> Union[Optional["DictAny"], None]:
        value = self.redis.get(key, **kwargs)
        return orjson.loads(value) if value else None

    async def set(
        self, key: str, value: "DictAny", expire: Optional[int], **kwargs: "DictAny"
    ) -> None:
        self.redis.set(key, orjson.dumps(value), expire, **kwargs)

    async def delete(self, key: str, **kwargs: "DictAny") -> Any:
        return self.redis.delete(key, **kwargs)


class AioRedisSessionBackend(SessionBackend):
    """
    Backend for aioredis.
    """

    redis: Optional[AioRedis]

    def __init__(self, redis: AioRedis, **kwargs) -> None:
        super().__init__(**kwargs)
        self.redis = redis

    async def get(self, key: str, **kwargs: "DictAny") -> Union[Optional["DictAny"], None]:
        value = await self.redis.get(key, **kwargs)
        return orjson.loads(value) if value else None

    async def set(
        self, key: str, value: "DictAny", expire: Optional[int], **kwargs: "DictAny"
    ) -> Optional[str]:
        return await self.redis.set(key, orjson.dumps(value), expire, **kwargs)

    async def delete(self, key: str, **kwargs: "DictAny") -> Any:
        return await self.redis.delete(key, **kwargs)


class MemCacheSessionBackend(SessionBackend):
    memcache: Optional[MemCache]

    def __init__(self, memcache: MemCache, **kwargs: "DictAny") -> None:
        super().__init__(**kwargs)
        self.memcache = memcache
        self.memcache.serde = MemCacheJSONSerde()

    async def get(self, key: str, **kwargs: "DictAny") -> Union[Optional["DictAny"], None]:
        value = self.memcache.get(key, **kwargs)
        return value if value else None

    async def set(
        self, key: str, value: "DictAny", expire: Optional[int], **kwargs: "DictAny"
    ) -> Optional[str]:
        return self.memcache.set(key, value, expire=expire, **kwargs)

    async def delete(self, key: str, **kwargs: "DictAny") -> Any:
        return self.memcache.delete(key, **kwargs)


class AioMemCacheSessionBackend(SessionBackend):
    memcache: Optional[AioMemcache]

    def __init__(self, memcache: AioMemcache, **kwargs: "DictAny") -> None:
        super().__init__(**kwargs)
        self.memcache = memcache
        self.memcache.serde = MemCacheJSONSerde()

    async def get(self, key: str, **kwargs: "DictAny") -> Union[Optional["DictAny"], None]:
        value = await self.memcache.get(key, **kwargs)
        return value if value else None

    async def set(
        self, key: str, value: "DictAny", expire: Optional[int], **kwargs: "DictAny"
    ) -> Optional[str]:
        return await self.memcache.set(key, value, expire=expire, **kwargs)

    async def delete(self, key: str, **kwargs: "DictAny") -> Any:
        return await self.memcache.delete(key, **kwargs)
