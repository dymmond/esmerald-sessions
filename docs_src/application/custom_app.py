from enums import BackendType
from esmerald import Esmerald, Gateway, get, post
from esmerald.requests import Request
from esmerald.responses import JSONResponse
from esmerald.utils.crypto import get_random_secret_key
from starlette.middleware import Middleware

from esmerald_sessions import SessionConfig, SessionMiddleware

from .backend import MyCustomBackend


@get()
async def view_session(request: Request) -> JSONResponse:
    return JSONResponse({"session": request.session})


@post()
async def setup_session(request: Request) -> JSONResponse:
    request.session.update({"data": "session.data"})
    return JSONResponse({"session": request.session})


@post()
async def clear_session(request: Request) -> JSONResponse:
    request.session.clear()
    return JSONResponse({"session": request.session})


custom_client = MyCustomBackend(...)
session_config = SessionConfig(
    secret_key=get_random_secret_key(),
    cookie_name="cookie",
    backend_type=BackendType.redis,
    custom_session_backend=custom_client,
)

app = Esmerald(
    routes=[
        Gateway("/view-session", handler=view_session),
        Gateway("/setup-session", handler=setup_session),
        Gateway("/clear-session", handler=clear_session),
    ],
    middleware=[Middleware(SessionMiddleware, config=session_config)],
)
