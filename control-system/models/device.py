from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.orm import relationship

from core.db import Base


class DeviceModel(Base):
    __tablename__ = "device"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    mqtt_topic = Column(String)
    control_type = Column(String)
    serial_number = Column(String, unique=True)
    lighting_class = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)

    data = relationship("DeviceDataModel", back_populates="device")
