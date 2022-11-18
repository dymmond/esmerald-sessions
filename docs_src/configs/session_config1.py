from esmerald import Esmerald
from esmerald.utils.crypto import get_random_secret_key
from redis import Redis
from starlette.middleware import Middleware

from esmerald_sessions import SessionConfig, SessionMiddleware
from esmerald_sessions.enums import BackendType

redis_client = Redis(host="localhost", port=6379)
session_config = SessionConfig(
    secret_key=get_random_secret_key(),
    cookie_name="cookie",
    backend_type=BackendType.redis,
    backend_client=redis_client,
)

app = Esmerald(
    routes=[...],
    middleware=[Middleware(SessionMiddleware, config=session_config)],
)
