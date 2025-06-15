from fastapi import APIRouter, Depends, Request

from core.dependencies.service import (
    get_device_data_service,
)
from schemas.base import PaginatedResponse
from schemas.device_data import (
    DeviceDataCreateSchema,
    DeviceDataQueryParams,
    DeviceDataSchema,
)
from schemas.pagination import PaginationParams
from services.device_data import DeviceDataService

router = APIRouter(prefix='/device-data', tags=['DevicesData'])  # noqa: F821

@router.get("/", response_model=PaginatedResponse[DeviceDataSchema])
async def get_all(
    request: Request,
    params: DeviceDataQueryParams = Depends(),
    pagination: PaginationParams = Depends(),
    service: DeviceDataService = Depends(get_device_data_service)
):
    return service.get_all(request=request, page=pagination.page, page_size=pagination.page_size, params=params.to_schema())

@router.get("/{item_id}", response_model=DeviceDataSchema)
async def get_by_id(item_id: int, params: DeviceDataQueryParams = Depends(), service:  DeviceDataService = Depends(get_device_data_service)):
    return service.get_by_id(item_id, params=params.to_schema()) 

@router.post("/", response_model=DeviceDataSchema)
async def create(item: DeviceDataCreateSchema, service: DeviceDataService = Depends(get_device_data_service)):
    return service.create(item)

@router.put("/{item_id}", response_model=DeviceDataSchema)
async def update(item_id: int, item: DeviceDataSchema, service: DeviceDataService = Depends(get_device_data_service)):
    return service.update(item_id, item)