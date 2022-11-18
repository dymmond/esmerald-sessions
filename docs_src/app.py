from esmerald import Esmerald, Gateway, get, post
from esmerald.requests import Request
from esmerald.responses import JSONResponse


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


app = Esmerald(
    routes=[
        Gateway("/view-session", handler=view_session),
        Gateway("/setup-session", handler=setup_session),
        Gateway("/clear-session", handler=clear_session),
    ],
)
