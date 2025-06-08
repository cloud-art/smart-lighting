from datetime import UTC, datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from core.db import Base


class DeviceDataModel(Base):
    __tablename__ = "device_data"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.now(tz=UTC))
    device_id = Column(Integer, ForeignKey("device.id"))
    car_count = Column(Integer)
    traffic_speed = Column(Float)
    traffic_density = Column(Float)
    pedestrian_count = Column(Integer)
    pedestrian_density = Column(Float)
    ambient_light = Column(Float)
    dimming_level = Column(Float)
    lamp_power = Column(Float)
    weather = Column(String)

    data = relationship("DeviceDataCalculatedDim", back_populates="device_data_id")
    data = relationship("DeviceDataCorrectedDim", back_populates="device_data_id")
