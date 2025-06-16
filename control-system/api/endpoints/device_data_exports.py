from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends

from core.dependencies.service import get_device_data_export_service
from services.device_data_exports import DeviceDataExportsService

router = APIRouter(prefix="/export", tags=["DeviceDataExport"])


@router.get("/device_data_csv/")
def device_data_csv(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    device: Optional[int] = None,
    service: DeviceDataExportsService = Depends(get_device_data_export_service),
):
    return service.export_to_csv(
        start_date=start_date, end_date=end_date, device=device
    )
