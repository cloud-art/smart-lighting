from celery_app import app
from core.logger import logger
from core.mqtt import Command
from schemas.device_data import DeviceDataCreateSchema
from services.dim_calculator import DimmingCalculator
from services.mqtt.types import IMQTTClient
from tasks.db_operations import DeviceDataDBService


@app.task(bind=True, max_retries=3)
def handle_mqtt_device_data_message(self, device_data_create: DeviceDataCreateSchema, mqtt_client: IMQTTClient):
    try:
        device_data = DeviceDataDBService.save_device_data(device_data_create)

        dim_level = DimmingCalculator.calculate(device_data)
        payload = mqtt_client.create_payload(Command.SET_DIMMING, dim_level)
        topic = mqtt_client.get_device_publish_topic(device_data)
        mqtt_client.publish(topic, payload)

        DeviceDataDBService.save_calculated_dim(
            {"device_data_id": device_data.id, "dimming_level": dim_level}
        )

    except Exception as e:
        logger.error(f"Error handling MQTT message: {e}")
        self.retry(exc=e, countdown=60)
