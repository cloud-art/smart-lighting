from typing import List

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from models.device_data import DeviceDataModel
from schemas.device_data import DeviceDataCreateSchema, DeviceDataSchema


class DeviceDataRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, data: DeviceDataCreateSchema) -> DeviceDataSchema:
        db_item = DeviceDataModel(**data.model_dump())
        self.db.add(db_item)
        self.db.commit()
        self.db.refresh(db_item)
        return DeviceDataSchema.model_validate(db_item)

    def get_by_id(self, item_id: int) -> DeviceDataSchema | None:
        db_item = (
            self.db.query(DeviceDataModel).filter(DeviceDataModel.id == item_id).first()
        )
        return DeviceDataSchema.model_validate(db_item) if db_item else None

    def get_all(self) -> list[DeviceDataSchema]:
        items = self.db.query(DeviceDataModel).all()
        return [DeviceDataSchema.model_validate(item) for item in items]

    def get_all_paginated(self, page: int, page_size: int) -> List[DeviceDataSchema]:
        offset = (page - 1) * page_size
        result = self.db.execute(
            select(DeviceDataModel)
            .order_by(DeviceDataModel.id)
            .offset(offset)
            .limit(page_size)
        )
        scalar = result.scalars().all()
        return [DeviceDataSchema.model_validate(item) for item in scalar]

    def get_total_count(self) -> int:
        return self.db.scalar(select(func.count()).select_from(DeviceDataModel))
