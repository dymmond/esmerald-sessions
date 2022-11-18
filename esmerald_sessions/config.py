from typing import Any, Optional

from pydantic import BaseModel

from esmerald_sessions.enums import BackendType
from esmerald_sessions.protocols import SessionBackend


class SessionConfig(BaseModel):
    """
    Configuration used to pass information for the SessionMiddleware.

    Args:
        secret_key: The secret key to use.
        path: The path for the cookie (Defaults to '/').
        cookie_name: The name of the cookie used to store the session id.
        max_age: The Max-Age of the cookie (defaults to 14 days).
        same_site: The SameSite attribute of the cookie (defaults to lax).
        https_only: Wether the cookie is https only or not. Recommended True if wanting to avoid
        the javascript from accessing the cookie.
        domain: The domain associated to the cookie (Default to None).
        backend_type: The type of predefined backend to use (Default to None,
            if None we'll use a regular cookie backend).
        backend_client: The client to use in the predefined backend. See examples for examples
            with predefined backends (Default to None).
        custom_session_backend: A custom backend that implements the SessionBackend.
    """

    secret_key: str
    path: Optional[str] = "/"
    cookie_name: str
    max_age: int = 14 * 24 * 60 * 60
    https_only: bool = False
    same_site: str = "lax"
    domain: Optional[str] = None
    backend_type: Optional[BackendType] = None
    backend_client: Optional[Any] = None
    custom_session_backend: Optional[SessionBackend] = None
