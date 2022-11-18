from base64 import b64decode, b64encode
from typing import TYPE_CHECKING, Optional
from uuid import uuid4

import itsdangerous
import orjson
from esmerald.datastructures import MutableHeaders
from esmerald.protocols import MiddlewareProtocol
from esmerald.requests import HTTPConnection
from esmerald.types import ASGIApp, Message, Receive, Scope, Send
from itsdangerous.exc import BadTimeSignature, SignatureExpired

from esmerald_sessions.backends import (
    AioMemCacheSessionBackend,
    AioRedisSessionBackend,
    MemCacheSessionBackend,
    RedisSessionBackend,
)
from esmerald_sessions.config import SessionConfig
from esmerald_sessions.enums import BackendType, ScopeType
from esmerald_sessions.exceptions import UnknownPredefinedBackend
from esmerald_sessions.protocols import SessionBackend

if TYPE_CHECKING:
    from pydantic.typing import DictAny


class SessionMiddleware(MiddlewareProtocol):
    """
    The middleware object to be passed to Esmerald middleware.

    Example:
        from esmerald import Esmerald
        from esmerald_sessions.middleware import SessionMiddleware

        app = Esmerald(routes=..., middleware=[SessionMiddleware])
    """

    def __init__(self, app: "ASGIApp", config: "SessionConfig", **kwargs: "DictAny"):
        """The SessionMiddleware object.

        Args:
            app (ASGIApp): The ASGIApp
            config (SessionConfig): The configuration file.
        """
        super().__init__(app, **kwargs)
        self.app = app
        self.config = config
        self.backend_type = self.config.backend_type or BackendType.cookie
        self.session_backend = (
            self.config.custom_session_backend
            if self.config.custom_session_backend
            else self._get_predefined_session_backend(self.config.backend_client)
        )
        self.signer = itsdangerous.TimestampSigner(self.config.secret_key)
        self._cookie_session_id_field = "_cssid"

        self.security_flags = f"httponly; samesite={self.config.same_site}"
        if self.config.https_only:
            self.security_flags += "; secure"

    async def __call__(self, scope: "Scope", receive: "Receive", send: "Send") -> None:
        if scope["type"] not in (ScopeType.HTTP, ScopeType.WEBSOCKET):  # pragma: no cover
            await self.app(scope, receive, send)
            return

        connection = HTTPConnection(scope)
        initial_empty_session = True

        if self.config.cookie_name in connection.cookies:
            data = connection.cookies[self.config.cookie_name].encode("utf-8")
            try:
                if self.backend_type == BackendType.cookie or not self.session_backend:
                    data = self.signer.unsign(data, max_age=self.config.max_age)
                    scope["session"] = orjson.loads(b64decode(data))
                else:
                    data = self.signer.unsign(data, max_age=self.config.max_age)
                    session_key = orjson.loads(b64decode(data)).get(self._cookie_session_id_field)
                    scope["session"] = await self.session_backend.get(session_key)
                    scope["__session_key"] = session_key
                initial_empty_session = False
            except (BadTimeSignature, SignatureExpired):
                scope["session"] = {}
        else:
            scope["session"] = {}

        async def send_wrapper(message: Message, **kwargs: "DictAny") -> None:
            if message["type"] == "http.response.start":
                session_key = scope.pop("__session_key", str(uuid4()))

                if scope["session"]:
                    if self.backend_type == BackendType.cookie or not self.session_backend:
                        cookie_data = scope["session"]
                    else:
                        await self.session_backend.set(
                            session_key, scope["session"], self.config.max_age
                        )
                        cookie_data = {self._cookie_session_id_field: session_key}

                    data = b64encode(orjson.dumps(cookie_data))
                    data = self.signer.sign(data)

                    headers = MutableHeaders(scope=message)
                    header_value = self._construct_cookie(clear=False, data=data)
                    headers.append("Set-Cookie", header_value)

                elif not initial_empty_session:
                    if self.session_backend and self.backend_type != BackendType.cookie:
                        await self.session_backend.delete(session_key)

                    headers = MutableHeaders(scope=message)
                    header_value = self._construct_cookie(clear=True)
                    headers.append("Set-Cookie", header_value)

            await send(message)

        await self.app(scope, receive, send_wrapper)

    def _get_predefined_session_backend(self, backend_db_client) -> Optional["SessionBackend"]:
        if self.backend_type == BackendType.redis:
            return RedisSessionBackend(backend_db_client)
        elif self.backend_type == BackendType.cookie:
            return None
        elif self.backend_type == BackendType.aioRedis:
            return AioRedisSessionBackend(backend_db_client)
        elif self.backend_type == BackendType.memcache:
            return MemCacheSessionBackend(backend_db_client)
        elif self.backend_type == BackendType.aioMemcache:
            return AioMemCacheSessionBackend(backend_db_client)
        else:
            raise UnknownPredefinedBackend()

    def _construct_cookie(self, clear: bool = False, data=None) -> str:
        if clear:
            cookie = f"{self.config.cookie_name}=null; Path={self.config.path}; Expires=Thu, 01 Jan 1970 00:00:00 GMT; Max-Age=0; {self.security_flags}"
        else:
            cookie = f"{self.config.cookie_name}={data.decode('utf-8')}; Path={self.config.path}; Max-Age={self.config.max_age}; {self.security_flags}"
        if self.config.domain:
            cookie = f"{cookie}; Domain={self.config.domain}"
        return cookie
