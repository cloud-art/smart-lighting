from typing import TypedDict
from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from common import CONTROL_TYPE
from database import Base
from datetime import datetime,UTC

class DeviceDataDict(TypedDict):
    id: int
    timestamp: datetime
    serial_number: int
    control_type: CONTROL_TYPE
    latitude: float
    longitude: float
    car_count: int
    traffic_speed: float
    traffic_density: float
    pedestrian_count: int
    pedestrian_density: float
    ambient_light: float
    dimming_level: float
    lighting_class: str
    lamp_power: float
    weather: str

class DeviceData(Base):
    __tablename__ = "device_data"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.now(tz=UTC))
    serial_number = Column(Integer)
    control_type = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    car_count = Column(Integer)
    traffic_speed = Column(Float)
    traffic_density = Column(Float)
    pedestrian_count = Column(Integer)
    pedestrian_density = Column(Float)
    ambient_light = Column(Float)
    dimming_level = Column(Float)
    lighting_class = Column(String)
    lamp_power = Column(Float)
    weather = Column(String)

class DeviceDataCalculatedDim(Base):
    __tablename__ = "device_data_calculated_dim"

    device_data_id = Column(Integer, ForeignKey('device_data.id'), primary_key=True, index=True)
    dimming_level = Column(Float)

class DeviceDataCorrectedDim(Base):
    __tablename__ = "device_data_corrected_dim"

    device_data_id = Column(Integer, ForeignKey('device_data.id'), primary_key=True, index=True)
    dimming_level = Column(Float)