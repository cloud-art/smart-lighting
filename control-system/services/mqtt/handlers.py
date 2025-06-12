import json
from typing import Any

from paho.mqtt.client import MQTTMessage

from core.logger import logger
from schemas.device_data import DeviceDataCreateSchema
from schemas.mqtt_message import DeviceDataMessage
from services.mqtt.types import IMQTTClient
from tasks.mqtt import handle_mqtt_device_data_message


class MessageHandler:
    def __init__(self, mqtt_client: IMQTTClient):
        self.mqtt_client = mqtt_client

    async def handle_message(self, msg: MQTTMessage) -> None:
        try:
            payload = self._parse_payload(msg)
            message = DeviceDataMessage(**payload)
            device_data_create = message.to_device_data_create()

            logger.info(f"Processing message from {msg.topic}")
            await self._process_message(device_data_create)

        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON payload: {e}")
        except Exception as e:
            logger.error(f"Message handling failed: {e}")

    def _parse_payload(self, msg: MQTTMessage) -> Any:
        return json.loads(msg.payload.decode())

    async def _process_message(
        self, device_data_create: DeviceDataCreateSchema
    ) -> None:
        handle_mqtt_device_data_message.delay(device_data_create)
