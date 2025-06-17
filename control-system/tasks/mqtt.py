from typing import Callable

from sqlalchemy.orm import Session

from celery_app import app
from core.logger import logger
from core.mqtt import Command, get_device_publish_topic
from repositories.device import DeviceDataCalculatedDimRepository
from repositories.device_data import DeviceDataRepository
from schemas.device_data import DeviceDataSchema
from schemas.device_data_dim_info import (
    DeviceDataDimInfoSchema,
)
from schemas.mqtt import MQTTPayload
from schemas.mqtt_message import DeviceDataMessage
from services.dim_calculator import DimmingCalculator


@app.task
def handle_mqtt_device_data_create(
    device_data_message_dict: dict,
    publish_fn: Callable[[str, str], None],
    db: Session,
    dimming_calculator: DimmingCalculator,
):
    try:
        device_data_repo = DeviceDataRepository(db)
        calculated_dim_repo = DeviceDataCalculatedDimRepository(db)

        device_data_message = DeviceDataMessage.model_validate(device_data_message_dict)

        device_data_create = device_data_message.to_device_data_create()
        device_data_model = device_data_repo.create(device_data_create)
        device_data = DeviceDataSchema.model_validate(device_data_model)

        dim_level = dimming_calculator.calculate(device_data)
        payload = MQTTPayload(action=Command.SET_DIMMING, value=dim_level)
        payload_str = payload.model_dump_json()
        topic = get_device_publish_topic(device_data.device.id)
        publish_fn(topic, payload_str)

        calculated_dim_repo.create(
            DeviceDataDimInfoSchema(
                device_data_id=device_data.id, dimming_level=dim_level
            )
        )

    except Exception as e:
        logger.error(f"Error handling MQTT message: {e}")
