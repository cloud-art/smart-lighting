from datetime import datetime
from typing import List

from pydantic import BaseModel

from core.types import Weather
from schemas.device import DeviceSchema


class DeviceDataBaseSchema(BaseModel):
    timestamp: datetime
    car_count: int
    traffic_speed: float
    traffic_density: float
    pedestrian_count: int
    pedestrian_density: float
    ambient_light: float
    dimming_level: float
    lamp_power: float
    weather: Weather


class DeviceDataCreateSchema(DeviceDataBaseSchema):
    device: int


class DeviceDataSchema(DeviceDataBaseSchema):
    id: int
    device = DeviceSchema

    class Config:
        from_attributes = True


class DeviceDataSummarySchema(DeviceDataSchema):
    calculated_dimming_level: float | None
    corrected_dimming_level: float | None

    class Config:
        from_attributes = True


class DeviceDataSummaryResponse(BaseModel):
    page: int
    next: str | None
    count: int
    results: List[DeviceDataSummarySchema]


class DimmingLevelUpdateResponse(BaseModel):
    success: bool
    device_data_id: int
    corrected_dimming_level: float
