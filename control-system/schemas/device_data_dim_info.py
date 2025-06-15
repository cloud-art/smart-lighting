from typing import Optional

from fastapi import Query
from pydantic import BaseModel


class DeviceDataDimInfoSchema(BaseModel):
    device_data_id: int
    dimming_level: float


class DeviceDataDimInfoDBItem(DeviceDataDimInfoSchema):
    class Config:
        from_attributes = True

class DeviceDataDimInfoQueryParamsSchema(BaseModel):
    device: Optional[int]

class DeviceDataDimInfoQueryParams:
    def __init__(
        self,
        device: int = Query(None, description="Идентификатор устройства"),
    ):
        self.device = device

    def to_schema(self) -> DeviceDataDimInfoQueryParamsSchema:
        return DeviceDataDimInfoQueryParamsSchema(device=self.device)
    