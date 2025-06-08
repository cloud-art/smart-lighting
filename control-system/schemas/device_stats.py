from typing import Optional

from pydantic import BaseModel


class StatsBase(BaseModel):
    avg_car_count: Optional[float]
    avg_traffic_speed: Optional[float]
    avg_pedestrian_count: Optional[float]
    avg_dimming_level: Optional[float]
    avg_calculated_dim: Optional[float]
    avg_corrected_dim: Optional[float]


class HourlyStats(StatsBase):
    hour: int


class WeekdayStats(StatsBase):
    day: int
    day_name: str


class DailyStats(StatsBase):
    day_of_month: int
