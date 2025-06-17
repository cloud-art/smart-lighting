from pydantic import BaseModel

from core.types import Weather


class ModelInputData(BaseModel):
    car_count: int
    traffic_speed: float
    traffic_density: float
    pedestrian_count: int
    pedestrian_density: float
    ambient_light: int
    lighting_class: str
    weather: Weather
    hour: int
    day_of_week: int
    is_weekend: int

    class Config:
        extra = "forbid"
