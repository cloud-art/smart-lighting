from typing import Optional

from pydantic import BaseModel


class DeviceStatsRowSchema(BaseModel):
    avg_car_count: Optional[float]
    avg_traffic_speed: Optional[float]
    avg_pedestrian_count: Optional[float]
    avg_dimming_level: Optional[float]
    avg_calculated_dim: Optional[float]
    avg_corrected_dim: Optional[float]


class DeviceHourlyAveragesStats(DeviceStatsRowSchema):
    hour: int


class DeviceWeekdayAverageStats(DeviceStatsRowSchema):
    day: int
    day_name: str


class DeviceDailyAverageStats(DeviceStatsRowSchema):
    day_of_month: int
