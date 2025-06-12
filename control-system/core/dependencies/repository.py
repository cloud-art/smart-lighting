from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from core.dependencies.db import get_db
from repositories.device import (
    DeviceDataCalculatedDimRepository,
    DeviceDataCorrectedDimRepository,
    DeviceDataRepository,
    DeviceRepository,
)
from repositories.device_data_summary import DeviceDataSummaryRepository
from repositories.device_stats import DeviceStatsRepository


def get_device_data_repository(db: Session = Depends(get_db)) -> DeviceDataRepository:
    return DeviceDataRepository(db)


def get_device_data_calculated_dim_repository(
    db: Session = Depends(get_db),
) -> DeviceDataCalculatedDimRepository:
    return DeviceDataCalculatedDimRepository(db)


def get_device_data_corrected_dim_repository(
    db: Session = Depends(get_db),
) -> DeviceDataCorrectedDimRepository:
    return DeviceDataCorrectedDimRepository(db)


def get_device_data_summary_repository(
    db: Session = Depends(get_db),
) -> DeviceDataSummaryRepository:
    return DeviceDataRepository(db)


def get_device_stats_repository(db: Session = Depends(get_db)) -> DeviceStatsRepository:
    return DeviceDataRepository(db)


def get_device_repository(db: Session = Depends(get_db)) -> DeviceRepository:
    return DeviceRepository(db)


DeviceDataRepoDep = Annotated[DeviceDataRepository, Depends(get_device_data_repository)]
DeviceDataCalculatedDimRepoDep = Annotated[
    DeviceDataCalculatedDimRepository,
    Depends(get_device_data_calculated_dim_repository),
]
DeviceDataCorrectedDimRepoDep = Annotated[
    DeviceDataCorrectedDimRepository, Depends(get_device_data_corrected_dim_repository)
]
DeviceDataSummaryRepoDep = Annotated[
    DeviceDataSummaryRepository, Depends(get_device_data_summary_repository)
]
DeviceStatsRepoDep = Annotated[
    DeviceStatsRepository, Depends(get_device_stats_repository)
]
DeviceRepoDep = Annotated[DeviceRepository, Depends(get_device_repository)]
