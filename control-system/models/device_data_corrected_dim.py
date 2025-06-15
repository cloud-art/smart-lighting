from sqlalchemy import Column, Float, ForeignKey, Integer
from sqlalchemy.orm import relationship

from core.db import Base


class DeviceDataCorrectedDimModel(Base):
    __tablename__ = "device_data_corrected_dim"

    device_data_id = Column(
        Integer, ForeignKey("device_data.id"), primary_key=True, index=True
    )
    dimming_level = Column(Float)
    
    data = relationship("DeviceDataModel", back_populates="corrected_dimming_level")
