from typing import Any, Dict

from fastapi import APIRouter, Depends

from core.dependencies.service import get_device_service
from schemas.pagination import PaginationParams
from services.device import DeviceService

router = APIRouter()

router.get("/", response_model=Dict[str, Any])
def get_device_data(
    pagination: PaginationParams = Depends(),
    service: DeviceService = Depends(get_device_service)
):
    return service.get_all_paginated(pagination.page, pagination.page_size)
