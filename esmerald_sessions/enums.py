from enum import Enum


class BackendType(Enum):
    redis = "redis"
    aioRedis = "aioRedis"
    cookie = "cookie"
    memcache = "memcache"
    aioMemcache = "aioMemcache"


class ScopeType:
    HTTP = "http"
    WEBSOCKET = "websocket"
