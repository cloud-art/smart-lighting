from fastapi import Depends
from sqlalchemy.orm import Session

from core.config import settings
from core.dependencies.db import get_db
from services.ai_model import AiModel
from services.device import (
    DeviceDataCalculatedDimService,
    DeviceDataCorrectedDimService,
    DeviceDataService,
    DeviceService,
)


def get_ai_model() -> AiModel:
    return AiModel(settings.MODEL_PATH)


def get_device_data_service(db: Session = Depends(get_db)) -> DeviceDataService:
    return DeviceDataService(db)

def get_device_data_calculated_dim_service(db: Session = Depends(get_db)) -> DeviceDataCalculatedDimService:
    return DeviceDataCalculatedDimService(db)

def get_device_data_corrected_dim_service(db: Session = Depends(get_db)) -> DeviceDataCorrectedDimService:
    return DeviceDataCorrectedDimService(db)

def get_device_service(db: Session = Depends(get_db)) -> DeviceService:
    return DeviceService(db)