from sqlalchemy.orm import Session

from models.device_data import DeviceDataModel
from repositories.base import BaseCRUDRepository
from schemas.device_data import DeviceDataCreateSchema, DeviceDataSchema


class DeviceDataRepository(
    BaseCRUDRepository[DeviceDataModel, DeviceDataCreateSchema, DeviceDataSchema]
):
    def __init__(self, db: Session):
        super().__init__(db=db, model=DeviceDataModel)
