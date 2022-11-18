from typing import List

from esmerald import EsmeraldAPISettings
from esmerald.types import Middleware
from esmerald.utils.crypto import get_random_secret_key
from redis import Redis

from esmerald_sessions import BackendType, SessionConfig, SessionMiddleware


class AppSettings(EsmeraldAPISettings):
    secret_key: str = get_random_secret_key()

    @property
    def session_config(self) -> SessionConfig:
        redis = Redis(host="localhost", port=6379)
        return SessionConfig(
            secret_key=self.secret_key,
            cookie_name="cookie",
            backend_type=BackendType.redis,
            backend_client=redis,
        )

    @property
    def middleware(self) -> List["Middleware"]:
        session_middleware = Middleware(SessionMiddleware, config=self.session_config)
        return [session_middleware]
