from typing import Any


class SessionException(Exception):
    """
    Base exception for all Asyncz thrown error exceptions.
    """

    detail = None

    def __init__(self, *args: Any, detail: str = ""):
        if detail:
            self.detail = detail
        super().__init__(*(str(arg) for arg in args if arg), detail)

    def __repr__(self) -> str:
        if self.detail:
            return f"{self.__class__.__name__} - {self.detail}"
        return self.__class__.__name__

    def __str__(self) -> str:
        return "".join(self.args).strip()


class UnknownPredefinedBackend(SessionException):
    detail = "Unknown predefined backend."
