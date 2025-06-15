from fastapi import APIRouter, Body, Depends, Request

from core.dependencies.service import (
    get_device_data_summary_service,
)
from schemas.base import PaginatedResponse
from schemas.device_data import (
    DeviceDataSummaryBulkUpdateSchema,
    DeviceDataSummaryQueryParams,
    DeviceDataSummarySchema,
    DeviceDataSummaryUpdateSchema,
)
from schemas.pagination import PaginationParams
from services.device_data_summary import DeviceDataSummaryService

router = APIRouter(prefix="/device-data-summary", tags=["DevicesDataSummary"])


@router.get("/", response_model=PaginatedResponse[DeviceDataSummarySchema])
async def get_all(
    request: Request,
    params: DeviceDataSummaryQueryParams = Depends(),
    pagination: PaginationParams = Depends(),
    service: DeviceDataSummaryService = Depends(get_device_data_summary_service),
):
    return service.get_all(request=request, page=pagination.page, page_size=pagination.page_size, params=params.to_schema())


@router.get("/{item_id}", response_model=DeviceDataSummarySchema)
async def get_by_id(
    item_id: int,
    service: DeviceDataSummaryService = Depends(get_device_data_summary_service),
):
    return service.get_by_id(item_id)


@router.patch("/{item_id}", response_model=DeviceDataSummarySchema)
async def update(
    item_id: int,
    body: DeviceDataSummaryUpdateSchema = Body(),
    service: DeviceDataSummaryService = Depends(get_device_data_summary_service),
):
    return service.update(item_id, body)

@router.post("/bulk_update", response_model=int)
async def bulk_update(
    body: DeviceDataSummaryBulkUpdateSchema = Body(),
    service: DeviceDataSummaryService = Depends(get_device_data_summary_service),
):
    return service.bulk_update(body)
