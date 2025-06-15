from fastapi import APIRouter, Depends, Request

from core.dependencies.service import (
    get_device_data_service,
    get_device_data_summary_service,
    get_device_service,
)
from schemas.base import PaginatedResponse
from schemas.device import DeviceBaseSchema, DeviceSchema
from schemas.pagination import PaginationParams
from services.device import DeviceService

router = APIRouter(prefix="/device", tags=["Devices"])


@router.get("/", response_model=PaginatedResponse[DeviceSchema])
async def get_all(
    request: Request,
    pagination: PaginationParams = Depends(),
    service: DeviceService = Depends(get_device_service),
):
    return service.get_all(request=request, page=pagination.page, page_size=pagination.page_size)


@router.get("/{item_id}", response_model=DeviceSchema)
async def get_by_id(item_id: int, service: DeviceService = Depends(get_device_service)):
    return service.get_by_id(item_id)


@router.post("/", response_model=DeviceSchema)
async def create(
    item: DeviceBaseSchema, service: DeviceService = Depends(get_device_service)
):
    return service.create(item)


@router.put("/{item_id}", response_model=DeviceSchema)
async def update(
    item_id: int,
    item: DeviceSchema,
    service: DeviceService = Depends(get_device_service),
):
    return service.update(item_id, item)
