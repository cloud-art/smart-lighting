from sqlalchemy import Column, Integer, Float, String, DateTime
from database import Base
from datetime import datetime

class DeviceData(Base):
    __tablename__ = "device_data"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    latitude = Column(Float)
    longitude = Column(Float)
    car_count = Column(Integer)
    car_speed = Column(Float)
    car_density = Column(Float)
    pedestrian_count = Column(Integer)
    pedestrian_density = Column(Float)
    road_luminance = Column(Float)
    dimming_level = Column(Float)
    lighting_class = Column(String)
    lamp_power = Column(Float)
