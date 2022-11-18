from typing import Any, Union

import orjson
from pydantic import BaseModel

from esmerald_sessions.exceptions import SessionException


class MemCacheJSONSerde(BaseModel):
    def serialize(self, key: Union[str, int], value: Any) -> Any:
        """
        Marshalls the value with ORJSON.
        """
        if isinstance(value, str):
            return value, 1
        return orjson.dumps(value).decode("utf-8"), 2

    def deserialize(self, key: Union[str, int], value: Any, flags: int) -> Any:
        """
        Unmarshalls the value with ORJSON.
        """
        if flags == 1:
            return value
        elif flags == 2:
            return orjson.loads(value)

        raise SessionException(detail=f"Unknown flags for value: {flags}.")
