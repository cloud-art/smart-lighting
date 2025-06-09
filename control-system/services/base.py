from typing import Optional, Sequence

from pydantic import BaseModel

from repositories.crud_repository import Base, BaseCRUDRepository, HasIdProtocol


class BaseCRUDServiceSchema(BaseModel):
    class Config:
        from_attributes = True


class BaseCRUDService[
    ModelType: (Base, HasIdProtocol),
    InstanceSchemaType: BaseCRUDServiceSchema,
    CreateSchemaType: BaseModel,
]:
    def __init__(self, repository: BaseCRUDRepository[ModelType, CreateSchemaType]):
        self.repository = repository

    def create(self, data: CreateSchemaType) -> InstanceSchemaType:
        data = self.repository.create(data)
        return InstanceSchemaType.model_validate(data)

    def update(self, item_id: int, data: InstanceSchemaType) -> InstanceSchemaType:
        data = self.repository.update(item_id, data)
        return InstanceSchemaType.model_validate(data)

    def bulk_update(self, item_ids: Sequence[int], data: InstanceSchemaType) -> int:
        return self.repository.bulk_update(item_ids, data)

    def get_by_id(self, item_id: int) -> Optional[InstanceSchemaType]:
        data = self.repository.get_by_id(item_id)
        return [InstanceSchemaType.model_validate(data) if data else None]

    def get_all(self) -> list[InstanceSchemaType]:
        data = self.repository.get_all()
        return [InstanceSchemaType.model_validate(item) for item in data]

    def get_all_paginated(self, page: int, page_size: int) -> list[InstanceSchemaType]:
        data = self.repository.get_all_paginated(page, page_size)
        return [InstanceSchemaType.model_validate(item) for item in data]

    def get_total_count(self) -> int:
        return self.repository.get_total_count()
