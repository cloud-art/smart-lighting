from sqlalchemy.orm import Session

from core.dependencies.db import get_db
from core.logger import logger
from models.device_data import DeviceDataModel
from models.device_data_calculated_dim import DeviceDataCalculatedDimModel
from schemas.device_data import DeviceDataCreateSchema, DeviceDataSchema
from schemas.device_data_dim_info import DeviceDataDimInfoDBItem


class DeviceDataDBService:
    @staticmethod
    def save_device_data(data: DeviceDataCreateSchema) -> DeviceDataSchema:
        db: Session = next(get_db())
        try:
            device_data = DeviceDataModel(**data.model_dump())
            db.add(device_data)
            db.commit()
            db.refresh(device_data)
            logger.info(f"Device data saved: {device_data.id}")
            return DeviceDataSchema.model_validate(device_data)
        except Exception as e:
            db.rollback()
            logger.error(f"Error saving device data: {e}")
            raise
        finally:
            db.close()

    @staticmethod
    def save_calculated_dim(data: dict) -> DeviceDataDimInfoDBItem:
        db: Session = next(get_db())
        try:
            dim_data = DeviceDataCalculatedDimModel(**data)
            db.add(dim_data)
            db.commit()
            db.refresh(dim_data)
            logger.info(f"Calculated dim saved: {dim_data.id}")
            return DeviceDataDimInfoDBItem.model_validate(dim_data)
        except Exception as e:
            db.rollback()
            logger.error(f"Error saving calculated dim: {e}")
            raise
        finally:
            db.close()
