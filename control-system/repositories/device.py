from sqlalchemy.orm import Session

from models.device import DeviceModel
from schemas.device import DeviceSchema


class DeviceRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, data: DeviceSchema) -> DeviceSchema:
        db_item = DeviceModel(**data.model_dump())
        self.db.add(db_item)
        self.db.commit()
        self.db.refresh(db_item)
        return DeviceSchema.model_validate(db_item)

    def get_by_id(self, item_id: int) -> DeviceSchema | None:
        db_item = self.db.query(DeviceModel).filter(DeviceModel.id == item_id).first()
        return DeviceSchema.model_validate(db_item) if db_item else None

    def get_all(self) -> list[DeviceSchema]:
        items = self.db.query(DeviceModel).all()
        return [DeviceSchema.model_validate(item) for item in items]
