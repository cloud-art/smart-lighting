from fastapi import Request
from sqlalchemy.orm import Session

from models.device_data import DeviceDataModel
from repositories.device import (
    DeviceDataCalculatedDimRepository,
)
from schemas.device_data_dim_info import (
    DeviceDataDimInfoDBItem,
    DeviceDataDimInfoQueryParams,
    DeviceDataDimInfoQueryParamsSchema,
    DeviceDataDimInfoSchema,
)
from services.base import BaseCRUDService


class DeviceDataCalculatedDimService:
    def __init__(self, db: Session):
        repository = DeviceDataCalculatedDimRepository(db)
        self.crud_service = BaseCRUDService[DeviceDataDimInfoDBItem](
            repository, DeviceDataDimInfoDBItem
        )

    def create(self, data: DeviceDataDimInfoSchema):
        return self.crud_service.create(data)

    def update(self, item_id: int, data: DeviceDataDimInfoDBItem):
        return self.crud_service.update(item_id=item_id, data=data)

    def get_by_id(self, item_id, params: DeviceDataDimInfoQueryParamsSchema):
        filters = {}
        joins = []
        if params.device:
            filters = {**filters, "data__device_id__eq": params.device}
            joins.append(("data", DeviceDataModel))

        return self.crud_service.get_by_id(
            item_id=item_id, filters=filters, joins=joins
        )

    def get_all(
        self,
        request: Request,
        params: DeviceDataDimInfoQueryParams,
        page: int,
        page_size: int,
    ):
        filters = {}
        joins = []
        if params.device is not None:
            filters = {**filters, "data__device_id__eq": params.device}
            joins.append(("data", DeviceDataModel))

        return self.crud_service.get_all(
            request=request,
            filters=filters,
            joins=joins,
            page=page,
            page_size=page_size,
        )
