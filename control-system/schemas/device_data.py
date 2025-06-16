from datetime import datetime
from typing import List, Optional

from fastapi import Query
from pydantic import BaseModel

from core.types import Weather
from schemas.base import BulkUpdateSchema
from schemas.device import DeviceSchema
from schemas.device_data_dim_info import DeviceDataDimInfoDBItem


class DeviceDataBaseSchema(BaseModel):
    timestamp: datetime
    car_count: int
    traffic_speed: float
    traffic_density: float
    pedestrian_count: Optional[int]
    pedestrian_density: Optional[float]
    ambient_light: Optional[float]
    dimming_level: Optional[float]
    lamp_power: Optional[float]
    weather: Optional[Weather]


class DeviceDataCreateSchema(DeviceDataBaseSchema):
    device_id: int


class DeviceDataSchema(DeviceDataBaseSchema):
    id: int
    device: DeviceSchema

    class Config:
        from_attributes = True


class DeviceDataQueryParamsSchema(BaseModel):
    device: Optional[int]


class DeviceDataQueryParams:
    def __init__(
        self,
        device: int = Query(None, description="Идентификатор устройства"),
    ):
        self.device = device

    def to_schema(self) -> DeviceDataQueryParamsSchema:
        return DeviceDataQueryParamsSchema(device=self.device)


class DeviceDataSummarySchema(DeviceDataSchema):
    calculated_dimming_level: Optional[DeviceDataDimInfoDBItem] = None
    corrected_dimming_level: Optional[DeviceDataDimInfoDBItem] = None

    class Config:
        from_attributes = True


class DeviceDataSummaryUpdateSchema(BaseModel):
    corrected_dimming_level: float | None


class DeviceDataSummaryBulkUpdateSchema(BulkUpdateSchema):
    corrected_dimming_level: float | None


class DeviceDataSummaryQueryParamsSchema(BaseModel):
    device: Optional[int]


class DeviceDataSummaryQueryParams:
    def __init__(
        self,
        device: int = Query(None, description="Идентификатор устройства"),
    ):
        self.device = device

    def to_schema(self) -> DeviceDataSummaryQueryParamsSchema:
        return DeviceDataSummaryQueryParamsSchema(device=self.device)


class DeviceDataSummaryResponse(BaseModel):
    page: int
    next: str | None
    count: int
    results: List[DeviceDataSummarySchema]


class DimmingLevelUpdateResponse(BaseModel):
    success: bool
    device_data_id: int
    corrected_dimming_level: float
