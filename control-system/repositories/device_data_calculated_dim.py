from sqlalchemy.orm import Session

from models.device_data_calculated_dim import DeviceDataCalculatedDimModel
from schemas.device_data_dim_info import (
    DeviceDataDimInfoDBItem,
    DeviceDataDimInfoSchema,
)


class DeviceDataCalculatedDimRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, data: DeviceDataDimInfoSchema) -> DeviceDataDimInfoDBItem:
        db_item = DeviceDataCalculatedDimModel(**data.model_dump())
        self.db.add(db_item)
        self.db.commit()
        self.db.refresh(db_item)
        return DeviceDataDimInfoDBItem.model_validate(db_item)

    def get_by_id(self, item_id: int) -> DeviceDataDimInfoDBItem | None:
        db_item = (
            self.db.query(DeviceDataCalculatedDimModel)
            .filter(DeviceDataCalculatedDimModel.id == item_id)
            .first()
        )
        return DeviceDataDimInfoDBItem.model_validate(db_item) if db_item else None

    def get_all(self) -> list[DeviceDataDimInfoDBItem]:
        items = self.db.query(DeviceDataCalculatedDimModel).all()
        return [DeviceDataDimInfoDBItem.model_validate(item) for item in items]
