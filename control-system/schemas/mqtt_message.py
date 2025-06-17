from datetime import datetime

from pydantic import BaseModel

from schemas.device_data import DeviceDataCreateSchema


class DeviceDataMessage(BaseModel):
    timestamp: str
    device: int
    car_count: int
    traffic_speed: float
    traffic_density: float
    pedestrian_count: int
    pedestrian_density: float
    ambient_light: int
    dimming_level: int
    lamp_power: float
    weather: str

    def to_device_data_create(self) -> DeviceDataCreateSchema:
        return DeviceDataCreateSchema(
            timestamp=datetime.fromisoformat(self.timestamp),
            device_id=int(self.device),
            car_count=self.car_count,
            traffic_speed=self.traffic_speed,
            traffic_density=self.traffic_density,
            pedestrian_count=self.pedestrian_count,
            pedestrian_density=self.pedestrian_density,
            ambient_light=float(self.ambient_light),
            dimming_level=float(self.dimming_level),
            lamp_power=self.lamp_power,
            weather=self.weather,
        )
