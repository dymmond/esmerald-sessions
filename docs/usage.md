# Usage

Using the package is actually very simple since it is prepared to handle the way Esmerald works, so it
fits withihn your application in the same way you add any other middleware to the application.

## How to use it

There are many ways you can plug Esmerald Sessions into your application. For the examples, let us use `Redis`.

### Within the instantiation

Esmerald being a system that is versatile allows you to add the middleware within the application instance.

```python
{!> ../docs_src/application/example1.py !}
```

### Using add_middleware

You can also add the middleware in the classic and sometimes familiar way as well.

```python
{!> ../docs_src/application/example2.py !}
```

### Using the settings

The Esmerald settings system makes this process even cleaner for your application.

Let's create the settings.

```python title='settings.py'
{!> ../docs_src/application/settings.py !}
```

Now let's create the application in a `main.py`.

```python title='main.py'
{!> ../docs_src/app.py !}
```

Now let's start the application.

```shell
ESMERALD_SETTINGS_MODULE=settings.AppSettings python -m main:app
```

!!! Check
    Because Esmerald works really well with settings and uses the `ESMERALD_SETTINGS_MODULE` that means you don't need
    to add the middleware as we with the [instantiation](#within-the-instantiation) or with
    [add_middleware](#using-add_middleware) because once the application starts it will loads the middlewares
    from your `AppSettings`.

Once the application starts, you should have an output in the console similar to this:

```shell
INFO:     Uvicorn running on http://localhost:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [4623] using WatchFiles
INFO:     Started server process [4625]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

