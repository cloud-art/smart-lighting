from sqlalchemy.orm import Session

from repositories.device import (
    DeviceRepository,
)
from schemas.device import DeviceSchema
from services.base import BaseCRUDService


class DeviceService(BaseCRUDService[DeviceSchema]):
    def __init__(self, db: Session):
        repository = DeviceRepository(db)
        super().__init__(repository, DeviceSchema)


