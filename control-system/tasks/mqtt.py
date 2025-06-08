from db_operations import DeviceDataDBService
from device_data import process_device_data_dim_level

from celery import app
from core.logger import logger
from schemas.device_data import DeviceDataCreateSchema


@app(bind=True, max_retries=3)
def handle_mqtt_device_data_message(self, device_data_create: DeviceDataCreateSchema):
    try:
        saved_data = DeviceDataDBService.save_device_data(device_data_create)
        process_device_data_dim_level.delay(saved_data)

    except Exception as e:
        logger.error(f"Error handling MQTT message: {e}")
        self.retry(exc=e, countdown=60)
