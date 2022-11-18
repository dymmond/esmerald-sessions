# Custom Backend

You can also implement your own backend for your Esmerald application as well. The way of doing it is by subclassing
the `SessionBackend` from the package and implement the methods.

## SessionBackend

Main class of all available backends from Esmerald Sessions.

```python
from esmerald_sessions import SessionBackend
```

## Available backends

Esmerald Sessions brings some built-in backends to be used within any Esmerald application.

### AioMemCacheSessionBackend

```python
from esmerald_sessions import AioMemCacheSessionBackend
```

### AioRedisSessionBackend

```python
from esmerald_sessions import AioRedisSessionBackend
```

### MemCacheSessionBackend

```python
from esmerald_sessions import MemCacheSessionBackend
```

### RedisSessionBackend

```python
from esmerald_sessions import RedisSessionBackend
```


### Implement a custom backend

As mentioned before, all the custom backends **must** inherit from `SessionBackend` and implement the methods.

```python
{!> ../docs_src/application/custom_backend.py !}
```

#### Example

```python title='backend.py'
{!> ../docs_src/application/example_custom_backend.py !}
```

Now we can add the new client to the application.

```python title='backend.py' hl_lines="10 30 34-35 44"
{!> ../docs_src/application/custom_app.py !}
```

As you can see, the difference between the built-in backends and the custom is the fact that the custom
**should always** be passed into the **custom_session_backend** property.
