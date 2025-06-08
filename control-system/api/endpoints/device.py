from typing import Any, Dict

from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session

from core.dependencies import get_db
from services.device import DeviceService

router = APIRouter()

router.get("/device/", response_model=Dict[str, Any])


def get_device_data(
    request: Request,
    db: Session = Depends(get_db),
    page: int = Query(1, description="Номер страницы", ge=1),
    page_size: int = Query(
        10, description="Количество записей на странице", ge=1, le=100
    ),
):
    return DeviceService.get_device_data(db, request, page, page_size)
