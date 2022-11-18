from typing import TYPE_CHECKING, Any, Optional

from esmerald_sessions import SessionBackend

if TYPE_CHECKING:
    from pydantic.typing import DictAny


class Client:
    # Your new client and logic here
    ...


class MyCustomBackend(SessionBackend):
    client: Optional[Client]

    def __init__(self, client: Client, **kwargs: "DictAny") -> None:
        super().__init__(**kwargs)
        self.client = client

    async def get(self, key: str, **kwargs: "DictAny") -> Optional["DictAny"]:
        value = await self.client.get(key, **kwargs)
        return value if value else None

    async def set(
        self, key: str, value: "DictAny", expire: Optional[int], **kwargs: "DictAny"
    ) -> Optional[str]:
        return await self.client.set(key, value, expire=expire, **kwargs)

    async def delete(self, key: str, **kwargs: "DictAny") -> Any:
        return await self.client.delete(key, **kwargs)
