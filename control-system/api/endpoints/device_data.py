from typing import Any, Dict, List

from fastapi import APIRouter, Body, Depends, Query, Request
from sqlalchemy.orm import Session

from core.dependencies import get_db
from schemas.device_data import DimmingLevelUpdateResponse
from services.device_data import DeviceDataService

router = APIRouter()

router.get("/device_data/", response_model=Dict[str, Any])


def get_device_data(
    request: Request,
    db: Session = Depends(get_db),
    page: int = Query(1, description="Номер страницы", ge=1),
    page_size: int = Query(
        10, description="Количество записей на странице", ge=1, le=100
    ),
):
    return DeviceDataService.get_device_data(db, request, page, page_size)


@router.get("/api/device_data_calculated_dim/", response_model=Dict[str, Any])
def get_device_data_calculated_dim(
    request: Request,
    db: Session = Depends(get_db),
    page: int = Query(1, description="Номер страницы", ge=1),
    page_size: int = Query(
        10, description="Количество записей на странице", ge=1, le=100
    ),
):
    return DeviceDataService.get_device_data_calculated_dim(
        db, request, page, page_size
    )


@router.get("/api/device_data_corrected_dim/", response_model=Dict[str, Any])
def get_device_data_calculated_dim(
    request: Request,
    db: Session = Depends(get_db),
    page: int = Query(1, description="Номер страницы", ge=1),
    page_size: int = Query(
        10, description="Количество записей на странице", ge=1, le=100
    ),
):
    return DeviceDataService.get_device_data_corrected_dim(db, request, page, page_size)


@router.get("/device_data_summary/", response_model=Dict[str, Any])
def get_device_data_summary(
    request: Request,
    db: Session = Depends(get_db),
    page: int = Query(1, description="Номер страницы", ge=1),
    page_size: int = Query(
        10, description="Количество записей на странице", ge=1, le=100
    ),
):
    return DeviceDataService.get_device_data_summary(db, request, page, page_size)


@router.patch(
    "/device_data_summary/{device_data_id}", response_model=DimmingLevelUpdateResponse
)
async def update_corrected_dimming_level(
    device_data_id: int, request: Request, db: Session = Depends(get_db)
):
    body = await request.json()
    corrected_dimming_level = body.get("corrected_dimming_level")

    return DeviceDataService.update_corrected_dimming_level(
        db=db,
        device_data_id=device_data_id,
        corrected_dimming_level=corrected_dimming_level,
    )


@router.post("/device_data_summary/bulk_update/")
async def bulk_update_corrected_dimming_level(
    updates: List[Dict[str, Any]] = Body(), db: Session = Depends(get_db)
):
    return DeviceDataService.bulk_update_corrected_dimming(db, updates)
