from fastapi import Depends
from sqlalchemy.orm import Session

from core.dependencies.db import get_db
from services.device import (
    DeviceService,
)
from services.device_data import DeviceDataService
from services.device_data_calculated_dim import DeviceDataCalculatedDimService
from services.device_data_corrected_dim import DeviceDataCorrectedDimService
from services.device_data_exports import DeviceDataExportsService
from services.device_data_summary import DeviceDataSummaryService
from services.device_stats import DeviceStatsService


def get_device_data_service(db: Session = Depends(get_db)) -> DeviceDataService:
    return DeviceDataService(db)


def get_device_data_summary_service(db: Session = Depends(get_db)) -> DeviceDataService:
    return DeviceDataSummaryService(db)


def get_device_data_calculated_dim_service(
    db: Session = Depends(get_db),
) -> DeviceDataCalculatedDimService:
    return DeviceDataCalculatedDimService(db)


def get_device_data_corrected_dim_service(
    db: Session = Depends(get_db),
) -> DeviceDataCorrectedDimService:
    return DeviceDataCorrectedDimService(db)


def get_device_service(db: Session = Depends(get_db)) -> DeviceService:
    return DeviceService(db)


def get_device_stats_service(db: Session = Depends(get_db)) -> DeviceStatsService:
    return DeviceStatsService(db)


def get_device_data_export_service(
    db: Session = Depends(get_db),
) -> DeviceDataExportsService:
    return DeviceDataExportsService(db)
