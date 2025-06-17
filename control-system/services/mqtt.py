import asyncio
import json
from typing import Any, Optional

from paho.mqtt.client import Client, MQTTMessage
from paho.mqtt.matcher import MQTTMatcher
from sqlalchemy.orm import Session

from core.config import settings
from core.logger import logger
from core.mqtt import DEVICE_RECIEVE_TOPIC, Command
from schemas.mqtt import MQTTPayload
from services.ai_model import AiModel
from services.dim_calculator import DimmingCalculator
from tasks.mqtt import handle_mqtt_device_data_create


class MQTTClient:
    def __init__(self, db: Session, ai_model: AiModel):
        self.client = Client()
        self._loop: Optional[asyncio.AbstractEventLoop] = None
        self.dimming_calculator = DimmingCalculator(ai_model=ai_model)
        self._handler = MessageHandler(self, db, self.dimming_calculator)
        self._configure_client()

    def _configure_client(self) -> None:
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        self.client.username_pw_set(settings.MQTT_USER, settings.MQTT_PASS)

    async def start(self) -> None:
        self._loop = asyncio.get_running_loop()
        logger.info(f"Connecting to {settings.MQTT_BROKER}:{settings.MQTT_PORT}...")

        try:
            self.client.connect(
                settings.MQTT_BROKER, settings.MQTT_PORT, settings.MQTT_KEEPALIVE
            )
            self.client.loop_start()
            logger.info("MQTT client started successfully")
        except Exception as e:
            logger.error(f"Failed to start MQTT client: {e}")
            raise

    def _on_connect(self, client: Client, userdata, flags, rc: int) -> None:
        if rc == 0:
            logger.info("Connected to MQTT Broker!")
            client.subscribe(DEVICE_RECIEVE_TOPIC)
        else:
            logger.error(f"Connection failed with code {rc}")

    def _on_message(self, client: Client, userdata, msg: MQTTMessage) -> None:
        try:
            logger.debug(f"Message received on {msg.topic}")
            self._handler.handle_message(msg)
        except Exception as e:
            logger.error(f"Error processing message: {e}")

    def publish(self, topic: str, payload: str, qos: int = 1) -> None:
        try:
            self.client.publish(topic=topic, payload=payload, qos=qos)
            logger.debug(f"Published to {topic}: {payload}")
        except Exception as e:
            logger.error(f"Failed to publish message: {e}")
            raise

    @staticmethod
    def create_payload(command: Command, value) -> str:
        payload = MQTTPayload(action=command, value=value)
        return payload.model_dump_json()


class MessageHandler:
    def __init__(
        self,
        mqtt_client: MQTTClient,
        db: Session,
        dimming_calculator: DimmingCalculator,
    ):
        self.mqtt_client = mqtt_client
        self.db = db
        self.dimming_calculator = dimming_calculator
        self.matcher = MQTTMatcher()
        self.matcher[DEVICE_RECIEVE_TOPIC] = "DEVICE_DATA_RECIEVE"

    def handle_message(self, msg: MQTTMessage) -> None:
        try:
            logger.info(f"Processing message from {msg.topic}")
            matched = self.matcher.iter_match(msg.topic)

            if next(matched, None) == "DEVICE_DATA_RECIEVE":
                self.handle_device_data_message(msg)
            else:
                logger.info("No one topic was proccessed")

        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON payload: {e}")
        except Exception as e:
            logger.error(f"Message handling failed: {e}")

    def handle_device_data_message(self, msg: MQTTMessage):
        payload = self._parse_payload(msg)
        handle_mqtt_device_data_create(
            payload,
            publish_fn=self.mqtt_client.publish,
            db=self.db,
            dimming_calculator=self.dimming_calculator,
        )

    def _parse_payload(self, msg: MQTTMessage) -> Any:
        return json.loads(msg.payload.decode())
