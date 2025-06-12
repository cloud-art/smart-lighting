from sqlalchemy.orm import Session

from models.device import DeviceModel
from models.device_data import DeviceDataModel
from models.device_data_calculated_dim import DeviceDataCalculatedDimModel
from models.device_data_corrected_dim import DeviceDataCorrectedDimModel
from repositories.base import BaseCRUDRepository
from schemas.device import DeviceBaseSchema, DeviceSchema
from schemas.device_data import DeviceDataCreateSchema, DeviceDataSchema
from schemas.device_data_dim_info import (
    DeviceDataDimInfoDBItem,
    DeviceDataDimInfoSchema,
)


class DeviceDataCalculatedDimRepository(
    BaseCRUDRepository[DeviceDataCalculatedDimModel, DeviceDataDimInfoSchema, DeviceDataDimInfoDBItem]
):
    def __init__(self, db: Session):
        super().__init__(db=db, model=DeviceDataCalculatedDimModel)


class DeviceDataCorrectedDimRepository(
    BaseCRUDRepository[DeviceDataCorrectedDimModel, DeviceDataDimInfoSchema, DeviceDataDimInfoDBItem]
):
    def __init__(self, db: Session):
        super().__init__(db=db, model=DeviceDataCorrectedDimModel)


class DeviceDataRepository(BaseCRUDRepository[DeviceDataModel, DeviceDataCreateSchema, DeviceDataSchema]):
    def __init__(self, db: Session):
        super().__init__(db=db, model=DeviceDataModel)


class DeviceRepository(BaseCRUDRepository[DeviceModel, DeviceBaseSchema, DeviceSchema]):
    def __init__(self, db: Session):
        super().__init__(db=db, model=DeviceModel)
