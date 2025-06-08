from fastapi import Depends

from celery import app
from core.dependencies import get_mqtt_client
from core.logger import logger
from core.mqtt import Command
from schemas.device_data import DeviceDataSchema
from schemas.mqtt_message import DeviceDataMessage
from services.dim_calculator import DimmingCalculator
from services.mqtt.client import MQTTClient
from tasks.db_operations import DeviceDataDBService


@app(bind=True, max_retries=3)
def process_device_data_dim_level(
    self,
    device_data: DeviceDataSchema,
    mqtt_client: MQTTClient = Depends(get_mqtt_client),
):
    try:
        dim_level = DimmingCalculator.calculate(device_data)

        payload = mqtt_client.create_payload(Command.SET_DIMMING, dim_level)
        topic = mqtt_client.get_device_publish_topic(device_data)
        mqtt_client.publish(topic, payload)

        DeviceDataDBService.save_calculated_dim(
            {"device_data_id": device_data.id, "dimming_level": dim_level}
        )

    except Exception as e:
        logger.error(f"Error processing device data: {e}")
        self.retry(exc=e, countdown=60)
