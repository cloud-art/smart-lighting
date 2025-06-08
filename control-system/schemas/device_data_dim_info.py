from pydantic import BaseModel


class DeviceDataDimInfoSchema(BaseModel):
    device_data_id: int
    dimming_level: float


class DeviceDataDimInfoDBItem(DeviceDataDimInfoSchema):
    id: int

    class Config:
        from_attributes = True
