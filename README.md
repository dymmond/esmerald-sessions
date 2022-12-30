# Esmerald

<p align="center">
  <a href="https://esmerald.dymmond.com"><img src="https://res.cloudinary.com/dymmond/image/upload/v1671718628/esmerald/img/logo-gr_oyr4my.png" alt='Esmerald'></a>
</p>

<p align="center">
    <em>🌟 An alternative SessionMiddleware for Esmerald with Pydantic at its core. 🌟</em>
</p>

<p align="center">
<a href="https://github.com/dymmond/esmerald-sessions/workflows/Test%20Suite/badge.svg?event=push&branch=main" target="_blank">
    <img src="https://github.com/dymmond/esmerald-sessions/workflows/Test%20Suite/badge.svg?event=push&branch=main" alt="Test Suite">
</a>

<a href="https://pypi.org/project/esmerald" target="_blank">
    <img src="https://img.shields.io/pypi/v/esmerald-sessions?color=%2334D058&label=pypi%20package" alt="Package version">
</a>

<a href="https://pypi.org/project/esmerald" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/esmerald-sessions.svg?color=%2334D058" alt="Supported Python versions">
</a>
</p>

---

**Documentation**: [https://esmerald-sessions.dymmond.com](https://esmerald-sessions.dymmond.com) 📚

**Source Code**: [https://github.com/dymmond/esmerald-sessions](https://github.com/dymmond/esmerald-sessions)

---

## Motivation

Using the default `SessionMiddleware` from Esmerald might not be enough for those applications that need a bit more
than just a simple caching, for example, where to store that same cookie.

This package offers that possibility and allows the extension of it if needed.

Inspired by [Starlette Session](https://github.com/auredentan/starlette-session/blob/master/starlette_session) and with
Pydantic at its core, Esmerald sessions offers the best of both worlds.

## Requirements

* Python 3.7+

## Installation

```shell
$ pip install esmerald-sessions
```

## How to use

Please check the [documentation](https://esmerald-sessions.dymmond.com) how to use the package.
