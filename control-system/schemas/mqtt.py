from typing import Any

from pydantic import BaseModel


class MQTTPayload(BaseModel):
    action: str
    value: Any
