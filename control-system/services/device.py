from sqlalchemy.orm import Session

from models.device import DeviceModel
from models.device_data import DeviceDataModel
from models.device_data_calculated_dim import DeviceDataCalculatedDimModel
from models.device_data_corrected_dim import DeviceDataCorrectedDimModel
from repositories.device import DeviceRepository
from repositories.device_data import DeviceDataRepository
from repositories.device_data_calculated_dim import DeviceDataCalculatedDimRepository
from repositories.device_data_corrected_dim import DeviceDataCorrectedDimRepository
from schemas.device import DeviceBaseSchema, DeviceSchema
from schemas.device_data import DeviceDataCreateSchema, DeviceDataSchema
from schemas.device_data_dim_info import (
    DeviceDataDimInfoDBItem,
    DeviceDataDimInfoSchema,
)
from services.base import BaseCRUDService


class DeviceDataService(
    BaseCRUDService[
        DeviceDataModel,
        DeviceDataSchema,
        DeviceDataCreateSchema,
    ]
):
    def __init__(self, db: Session):
        repository = DeviceDataRepository(db)
        super().__init__(repository)


class DeviceDataCalculatedDimService(
    BaseCRUDService[
        DeviceDataCalculatedDimModel,
        DeviceDataDimInfoDBItem,
        DeviceDataDimInfoSchema,
    ]
):
    def __init__(self, db: Session):
        repository = DeviceDataCalculatedDimRepository(db)
        super().__init__(repository)


class DeviceDataCorrectedDimService(
    BaseCRUDService[
        DeviceDataCorrectedDimModel,
        DeviceDataDimInfoDBItem,
        DeviceDataDimInfoSchema,
    ]
):
    def __init__(self, db: Session):
        repository = DeviceDataCorrectedDimRepository(db)
        super().__init__(repository)


class DeviceService(
    BaseCRUDService[
        DeviceModel,
        DeviceSchema,
        DeviceBaseSchema,
    ]
):
    def __init__(self, db: Session):
        repository = DeviceRepository(db)
        super().__init__(repository)
