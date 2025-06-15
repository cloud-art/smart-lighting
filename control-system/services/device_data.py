from fastapi import Request
from sqlalchemy.orm import Session

from repositories.device import (
    DeviceDataRepository,
)
from schemas.device_data import (
    DeviceDataBaseSchema,
    DeviceDataQueryParamsSchema,
    DeviceDataSchema,
)
from services.base import BaseCRUDService


class DeviceDataService():
    def __init__(self, db: Session):
        repository = DeviceDataRepository(db)
        self.crud_service = BaseCRUDService[DeviceDataSchema](repository, DeviceDataSchema)

    def create(self, data: DeviceDataBaseSchema):
        return self.crud_service.create(data)

    def update(self, item_id: int, data: DeviceDataSchema):
        return self.crud_service.update(item_id=item_id, data=data)

    def get_by_id(self, item_id, params: DeviceDataQueryParamsSchema):
        filters = {}
        if params.device:
            filters = {**filters, "device": params.device}

        return self.crud_service.get_by_id(
            item_id=item_id, filters=filters
        )

    def get_all(
        self,
        request: Request,
        params: DeviceDataQueryParamsSchema,
        page: int,
        page_size: int,
    ):
        filters = {}
        if params.device:
            filters = {**filters, "device": params.device}

        return self.crud_service.get_all(
            request=request,
            filters=filters,
            page=page,
            page_size=page_size,
        )

