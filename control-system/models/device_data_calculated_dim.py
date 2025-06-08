from sqlalchemy import Column, Float, ForeignKey, Integer

from core.db import Base


class DeviceDataCalculatedDimModel(Base):
    __tablename__ = "device_data_calculated_dim"

    device_data_id = Column(
        Integer, ForeignKey("device_data.id"), primary_key=True, index=True
    )
    dimming_level = Column(Float)
