from sqlalchemy.orm import Session

from core.dependencies.db import get_db
from core.logger import logger
from models.device_data import DeviceDataModel
from schemas.device_data import DeviceDataCreateSchema, DeviceDataSchema
from schemas.device_data_dim_info import DeviceDataDimInfoDBItem


class DeviceDataDBService:
    @staticmethod
    def save_device_data(data: DeviceDataCreateSchema) -> DeviceDataSchema:
        db: Session = next(get_db())
        try:
            device = DeviceDataModel(**data)
            db.add(device)
            db.commit()
            db.refresh(device)
            logger.info(f"Device data saved: {device.id}")
            return DeviceDataSchema.model_validate(device)
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
            dim_data = DeviceDataDimInfoDBItem(**data)
            db.add(dim_data)
            db.commit()
            db.refresh(dim_data)
            logger.info(f"Calculated dim saved: {dim_data.id}")
            return dim_data
        except Exception as e:
            db.rollback()
            logger.error(f"Error saving calculated dim: {e}")
            raise
        finally:
            db.close()
