from typing import TYPE_CHECKING, Any, Optional

from esmerald_sessions import SessionBackend

if TYPE_CHECKING:
    from pydantic.typing import DictAny


class MyCustomBackend(SessionBackend):
    async def get(self, key: str, **kwargs: "DictAny") -> Optional["DictAny"]:
        # Add logic here
        ...

    async def set(
        self, key: str, value: "DictAny", expire: Optional[int], **kwargs: "DictAny"
    ) -> Optional[str]:
        # Add logic here
        ...

    async def delete(self, key: str, **kwargs: "DictAny") -> Any:
        # Add logic here
        ...
