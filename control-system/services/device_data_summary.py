from fastapi import HTTPException, Request, status
from sqlalchemy.orm import Session

from repositories.device_data_summary import (
    DeviceDataSummaryRepository,
)
from schemas.device_data import (
    DeviceDataSummaryBulkUpdateSchema,
    DeviceDataSummaryQueryParamsSchema,
    DeviceDataSummarySchema,
    DeviceDataSummaryUpdateSchema,
)
from utils.pagination import Pagination


class DeviceDataSummaryService():
    def __init__(self, db: Session):
        self.repository = DeviceDataSummaryRepository(db)

    def update(self, item_id: int, data: DeviceDataSummaryUpdateSchema):
        result = self.repository.update(id=item_id, data=data)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error",
            )
        return DeviceDataSummarySchema.model_validate(result)

    def bulk_update(self, data: DeviceDataSummaryBulkUpdateSchema):
        update_data = DeviceDataSummaryUpdateSchema(**data.model_dump(exclude={"ids"}))
        return self.repository.bulk_update(ids=data.ids, data=update_data)

    def get_by_id(self, item_id):
        result = self.repository.get_by_id(id=item_id)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Not found",
            )
        return DeviceDataSummarySchema.model_validate(result)

    def get_all(
        self,
        request: Request,
        params: DeviceDataSummaryQueryParamsSchema,
        page: int,
        page_size: int,
    ):
        total_count = self.repository.get_total_count(device_id=params.device)

        result = self.repository.get_all(
            page=page, page_size=page_size, device_id=params.device
        )

        items = [DeviceDataSummarySchema.model_validate(item) for item in result]

        return Pagination.paginate(
            request=request,
            items=items,
            page=page,
            page_size=page_size,
            total_count=total_count,
        )
