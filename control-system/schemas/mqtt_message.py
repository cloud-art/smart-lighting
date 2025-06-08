from datetime import datetime

from pydantic import BaseModel

from core.types import LightingClass, Weather
from schemas.device_data import DeviceDataCreateSchema, DeviceDataSchema


class DeviceDataMessage(BaseModel):
    timestamp: str
    device: str
    car_count: str
    traffic_speed: str
    traffic_density: str
    pedestrian_count: str
    pedestrian_density: str
    ambient_light: str
    dimming_level: str
    lamp_power: str
    weather: str

    def to_device_data_create(self) -> DeviceDataCreateSchema:
        return DeviceDataSchema(
            timestamp=datetime.fromisoformat(self.timestamp),
            device_id=int(self.device_id),
            car_count=int(self.car_count),
            traffic_speed=float(self.traffic_speed),
            traffic_density=float(self.traffic_density),
            pedestrian_count=int(self.pedestrian_count),
            pedestrian_density=float(self.pedestrian_density),
            ambient_light=float(self.ambient_light),
            dimming_level=float(self.dimming_level),
            lamp_power=float(self.lamp_power),
            weather=self.weather,
        )
