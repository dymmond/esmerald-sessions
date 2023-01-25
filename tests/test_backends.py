import re

import fakeredis
import pytest
from esmerald_sessions.config import SessionConfig
from esmerald_sessions.datastructures import MemCacheJSONSerde
from esmerald_sessions.enums import BackendType
from esmerald_sessions.exceptions import SessionException
from esmerald_sessions.middleware import SessionMiddleware
from pymemcache.test.utils import MockMemcacheClient
from starlette.middleware import Middleware

from esmerald import Gateway, JSONResponse, Request, get, post
from esmerald.applications import Esmerald
from esmerald.testclient import EsmeraldTestClient, create_client
from esmerald.utils.crypto import get_random_secret_key


@get()
def view_session(request: Request) -> JSONResponse:
    return JSONResponse({"session": request.session})


@post()
async def update_session(request: Request) -> JSONResponse:
    data = await request.json()
    request.session.update(data)
    return JSONResponse({"session": request.session})


@post()
async def clear_session(request: Request) -> JSONResponse:
    request.session.clear()
    return JSONResponse({"session": request.session})


@pytest.fixture
def app():
    app = Esmerald(
        routes=[
            Gateway("/view-session", handler=view_session),
            Gateway("/update-session", handler=update_session),
            Gateway("/clear-session", handler=clear_session),
        ]
    )
    return app


@pytest.fixture
def redis() -> fakeredis.FakeStrictRedis:
    return fakeredis.FakeStrictRedis()


@pytest.fixture
def memcache():
    return MockMemcacheClient()


def test_MemcacheJSONSerde():
    serde = MemCacheJSONSerde()

    assert serde.serialize("key", "test") == ("test", 1)
    assert serde.serialize("key", {"key1": "test"}) == ('{"key1":"test"}', 2)
    assert serde.deserialize("key", "value", 1) == "value"
    assert serde.deserialize("key", '{"key1":"test"}', 2) == {"key1": "test"}

    with pytest.raises(SessionException):
        serde.deserialize("key", '{"key1":"test"}', -1)


def test_without_backend(app):
    session_config = SessionConfig(secret_key=get_random_secret_key(), cookie_name="cookie")
    app.add_middleware(SessionMiddleware, config=session_config)

    client = EsmeraldTestClient(app)

    response = client.get("/view-session")
    assert response.json() == {"session": {}}

    response = client.post("/update-session", json={"data": "something"})
    assert response.json() == {"session": {"data": "something"}}

    # check cookie max-age
    set_cookie = response.headers["set-cookie"]
    max_age_matches = re.search(r"; Max-Age=([0-9]+);", set_cookie)
    assert max_age_matches is not None
    assert int(max_age_matches[1]) == 14 * 24 * 3600

    response = client.post("/clear-session")
    assert response.json() == {"session": {}}


def test_without_backend_using_config():
    session_config = SessionConfig(secret_key=get_random_secret_key(), cookie_name="cookie")

    with create_client(
        routes=[
            Gateway("/view-session", handler=view_session),
            Gateway("/update-session", handler=update_session),
            Gateway("/clear-session", handler=clear_session),
        ],
        middleware=[Middleware(SessionMiddleware, config=session_config)],
    ) as client:

        response = client.get("/view-session")
        assert response.json() == {"session": {}}

        response = client.post("/update-session", json={"data": "something"})
        assert response.json() == {"session": {"data": "something"}}

        # check cookie max-age
        set_cookie = response.headers["set-cookie"]
        max_age_matches = re.search(r"; Max-Age=([0-9]+);", set_cookie)
        assert max_age_matches is not None
        assert int(max_age_matches[1]) == 14 * 24 * 3600

        response = client.post("/clear-session")
        assert response.json() == {"session": {}}


def test_with_redis_backend(mocker, app, redis):
    session_config = SessionConfig(
        secret_key=get_random_secret_key(),
        cookie_name="cookie",
        backend_type=BackendType.redis,
        backend_client=redis,
    )
    app.add_middleware(SessionMiddleware, config=session_config)
    client = EsmeraldTestClient(app)

    spy_redis_set = mocker.spy(redis, "set")
    spy_redis_get = mocker.spy(redis, "get")
    spy_redis_delete = mocker.spy(redis, "delete")

    response = client.get("/view-session")
    assert response.json() == {"session": {}}

    response = client.post("/update-session", json={"data": "something"})
    assert response.json() == {"session": {"data": "something"}}
    spy_redis_set.assert_called_once()

    response = client.get("/view-session")
    spy_redis_get.assert_called_once()

    response = client.post("/clear-session")
    assert response.json() == {"session": {}}
    spy_redis_delete.assert_called_once()


def test_with_redis_backend_with_config(mocker, app, redis):
    session_config = SessionConfig(
        secret_key=get_random_secret_key(),
        cookie_name="cookie",
        backend_type=BackendType.redis,
        backend_client=redis,
    )
    with create_client(
        routes=[
            Gateway("/view-session", handler=view_session),
            Gateway("/update-session", handler=update_session),
            Gateway("/clear-session", handler=clear_session),
        ],
        middleware=[Middleware(SessionMiddleware, config=session_config)],
    ) as client:
        spy_redis_set = mocker.spy(redis, "set")
        spy_redis_get = mocker.spy(redis, "get")
        spy_redis_delete = mocker.spy(redis, "delete")

        response = client.get("/view-session")
        assert response.json() == {"session": {}}

        response = client.post("/update-session", json={"data": "something"})
        assert response.json() == {"session": {"data": "something"}}
        spy_redis_set.assert_called_once()

        response = client.get("/view-session")
        spy_redis_get.assert_called_once()

        response = client.post("/clear-session")
        assert response.json() == {"session": {}}
        spy_redis_delete.assert_called_once()


def test_with_memcache_backend(mocker, app, memcache):

    session_config = SessionConfig(
        secret_key=get_random_secret_key(),
        cookie_name="cookie",
        backend_type=BackendType.memcache,
        backend_client=memcache,
    )
    app.add_middleware(SessionMiddleware, config=session_config)
    client = EsmeraldTestClient(app)

    spy_redis_set = mocker.spy(memcache, "set")
    spy_redis_get = mocker.spy(memcache, "get")
    spy_redis_delete = mocker.spy(memcache, "delete")

    response = client.get("/view-session")
    assert response.json() == {"session": {}}

    response = client.post("/update-session", json={"data": "something"})
    assert response.json() == {"session": {"data": "something"}}
    spy_redis_set.assert_called_once()

    response = client.get("/view-session")
    spy_redis_get.assert_called_once()

    response = client.post("/clear-session")
    assert response.json() == {"session": {}}
    spy_redis_delete.assert_called_once()


def test_with_memcache_backend_config(mocker, app, memcache):

    session_config = SessionConfig(
        secret_key=get_random_secret_key(),
        cookie_name="cookie",
        backend_type=BackendType.memcache,
        backend_client=memcache,
    )
    with create_client(
        routes=[
            Gateway("/view-session", handler=view_session),
            Gateway("/update-session", handler=update_session),
            Gateway("/clear-session", handler=clear_session),
        ],
        middleware=[Middleware(SessionMiddleware, config=session_config)],
    ) as client:

        spy_redis_set = mocker.spy(memcache, "set")
        spy_redis_get = mocker.spy(memcache, "get")
        spy_redis_delete = mocker.spy(memcache, "delete")

        response = client.get("/view-session")
        assert response.json() == {"session": {}}

        response = client.post("/update-session", json={"data": "something"})
        assert response.json() == {"session": {"data": "something"}}
        spy_redis_set.assert_called_once()

        response = client.get("/view-session")
        spy_redis_get.assert_called_once()

        response = client.post("/clear-session")
        assert response.json() == {"session": {}}
        spy_redis_delete.assert_called_once()
