# Session Config

Similar to the `SessionConfig` from Esmerald, this one follows the same principle and for that reason we kept the same
name to make it easier and faster to understand.

## The config class

The SessionConfig is used to pass the necessary parameters to the SessionMiddleware object with all the needed
parameters. Like every single configuration of Esmerald, this also uses **Pydantic** and leverages the power of the
library.

```python title='backend.py' hl_lines="10-15 19"
{!> ../docs_src/configs/session_config1.py !}
```

The way of passing the configurations is demonstrated in the [usage](./usage.md) section of the documentation with
more examples how to do it.

## Parameter

* **secret_key** - The string used for the encryption/decryption. We advise to use the same secret as the one in the
settings to make it consistent.

* **path** - The path for the cookie.

    <sup>Default: `/`</sup>

* **cookie_name** - The name for the session cookie.
* **max_age** - The number in seconds until the cookie expires.

    <sup>Default: `14 * 24 * 60 * 60` seconds</sup>

* **https_only** - Boolean if set enforces the session cookie to be httpsOnly.

    <sup>Default: `False`</sup>

* **same_site** - Level of restriction for the session cookie. 
<a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Set-Cookie/SameSite" target="_blank">
More on this</a>.

    <sup>Default: `lax`</sup>

* **domain** - The domain associated to the cookie.

    <sup>Default: `None`</sup>

* **backend_type** - String type of predefined backend to use.

    <sup>Default: `None`</sup>

* **backend_client** - The client to use in the predefined backend.

    <sup>Default: `None`</sup>

* **custom_session_backend** - A custom backend that implement [SessionBackend](./backends.md#sessionbackend).

    <sup>Default: `None`</sup>
