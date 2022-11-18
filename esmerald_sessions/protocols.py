from abc import ABC
from typing import TYPE_CHECKING, Any, Optional

from pydantic import BaseModel

if TYPE_CHECKING:
    from pydantic.typing import DictAny


class SessionBackend(BaseModel, ABC):
    """
    Base model class for any session backend.
    """

    async def get(self, key: str, **kwargs: "DictAny") -> Optional["DictAny"]:
        raise NotImplementedError()  # pragma: no cover

    async def set(
        self, key: str, value: "DictAny", expire: Optional[int], **kwargs: "DictAny"
    ) -> Optional[str]:
        raise NotImplementedError()  # pragma: no cover

    async def delete(self, key: str, **kwargs: "DictAny") -> Any:
        raise NotImplementedError()  # pragma: no cover

    class Config:
        arbitrary_types_allowed = True
