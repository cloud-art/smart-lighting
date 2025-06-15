
from fastapi import APIRouter, Depends, Request

from core.dependencies.service import (
    get_device_data_corrected_dim_service,
)
from schemas.base import PaginatedResponse
from schemas.device_data_dim_info import (
    DeviceDataDimInfoDBItem,
    DeviceDataDimInfoQueryParams,
    DeviceDataDimInfoSchema,
)
from schemas.pagination import PaginationParams
from services.device_data_corrected_dim import DeviceDataCorrectedDimService

router = APIRouter(
    prefix="/device-data-corrected-dim", tags=["DevicesDataCorrectedDim"]
)


@router.get("/", response_model=PaginatedResponse[DeviceDataDimInfoDBItem])
async def get_all(
    request: Request,
    params: DeviceDataDimInfoQueryParams = Depends(),
    pagination: PaginationParams = Depends(),
    service: DeviceDataCorrectedDimService = Depends(
        get_device_data_corrected_dim_service
    ),
):
    return service.get_all(
        request=request,
        page=pagination.page,
        page_size=pagination.page_size,
        params=params.to_schema()
    )


@router.get("/{item_id}", response_model=DeviceDataDimInfoDBItem)
async def get_by_id(
    item_id: int,
    params: DeviceDataDimInfoQueryParams = Depends(),
    service: DeviceDataCorrectedDimService = Depends(
        get_device_data_corrected_dim_service
    ),
):
    return service.get_by_id(
        item_id, params=params.to_schema()
    )


@router.post("/", response_model=DeviceDataDimInfoDBItem)
async def create(
    item: DeviceDataDimInfoSchema,
    service: DeviceDataCorrectedDimService = Depends(
        get_device_data_corrected_dim_service
    ),
):
    return service.create(item)


@router.put("/{item_id}", response_model=DeviceDataDimInfoDBItem)
async def update(
    item_id: int,
    item: DeviceDataDimInfoDBItem,
    service: DeviceDataCorrectedDimService = Depends(
        get_device_data_corrected_dim_service
    ),
):
    return service.update(item_id, item)
