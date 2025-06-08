from pydantic import BaseModel


class ModelInputData(BaseModel):
    timestamp: str
    serial_number: str
    car_count: int
    traffic_speed: float
    pedestrian_count: int
    ambient_light: float
    lighting_class: str
    hour: int
    day_of_week: int
    is_weekend: int

    class Config:
        extra = "forbid"
