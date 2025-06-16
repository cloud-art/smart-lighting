import asyncio
from typing import Optional

from paho.mqtt.client import Client, MQTTMessage

from core.config import settings
from core.logger import logger
from core.mqtt import Command
from schemas.mqtt import MQTTPayload
from services.mqtt.handlers import MessageHandler


class MQTTClient:
    def __init__(self):
        self.client = Client()
        self._loop: Optional[asyncio.AbstractEventLoop] = None
        self._handler = MessageHandler(self)
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
            client.subscribe(settings.MQTT_RECIEVE_TOPIC)
        else:
            logger.error(f"Connection failed with code {rc}")

    def _on_message(self, client: Client, userdata, msg: MQTTMessage) -> None:
        try:
            logger.debug(f"Message received on {msg.topic}")

            def sendMessageBack(dim_level: int, device_data):
                payload = self.create_payload(Command.SET_DIMMING, dim_level)
                topic = self.get_device_publish_topic(device_data)
                self.publish(topic, payload)

            self._loop.create_task(self._handler.handle_message(msg, sendMessageBack))
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

    @staticmethod
    def get_device_publish_topic(device):
        return "/control"
