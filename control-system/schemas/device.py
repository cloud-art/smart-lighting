from typing import List

from pydantic import BaseModel

from core.types import ControlType, LightingClass


class DeviceBaseSchema(BaseModel):
    control_type: ControlType
    serial_number: str
    lighting_class: LightingClass
    latitude: float
    longitude: float


class DeviceSchema(DeviceBaseSchema):
    id: int

    class Config:
        from_attributes = True


class DeviceResponse(BaseModel):
    page: int
    next: str | None
    count: int
    results: List[DeviceSchema]
