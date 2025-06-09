from typing import Any, Optional, Protocol, Sequence, Type, runtime_checkable

from pydantic import BaseModel
from sqlalchemy import func, select, update
from sqlalchemy.orm import DeclarativeBase, Session


class Base(DeclarativeBase):
    pass


@runtime_checkable
class HasIdProtocol(Protocol):
    id: Any


class BaseCRUDRepository[
    ModelType: (Base, HasIdProtocol),
    CreateSchemaType: BaseModel,
    UpdateSchemaType: BaseModel,
]:
    def __init__(self, db: Session, model: Type[ModelType]):
        self.db = db
        self.model = model

    def create(self, data: CreateSchemaType) -> ModelType:
        db_item = self.model(**data.model_dump())
        self.db.add(db_item)
        self.db.commit()
        self.db.refresh(db_item)
        return db_item

    def update(self, item_id: int, data: UpdateSchemaType) -> Optional[ModelType]:
        db_item = self.get_by_id(item_id)
        if db_item:
            for key, value in data.model_dump(exclude_unset=True).items():
                setattr(db_item, key, value)
            self.db.commit()
            self.db.refresh(db_item)
            return db_item
        return None

    def bulk_update(self, item_ids: Sequence[int], data: UpdateSchemaType) -> int:
        update_data = data.model_dump(exclude_unset=True)
        result = self.db.execute(
            update(self.model).where(self.model.id.in_(item_ids)).values(**update_data)
        )
        self.db.commit()
        return result.rowcount

    def get_by_id(self, item_id: int) -> Optional[ModelType]:
        db_item = self.db.query(self.model).filter(self.model.id == item_id).first()
        return db_item if db_item else None

    def get_all(self) -> list[ModelType]:
        items = self.db.query(self.model).all()
        return items

    def get_all_paginated(self, page: int, page_size: int) -> list[ModelType]:
        offset = (page - 1) * page_size
        result = self.db.execute(
            select(ModelType).order_by(ModelType.id).offset(offset).limit(page_size)
        )
        return result.scalars().all()

    def get_total_count(self) -> int:
        return self.db.scalar(select(func.count()).select_from(ModelType))
