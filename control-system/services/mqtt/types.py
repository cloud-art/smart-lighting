from typing import Any, Protocol

from paho.mqtt.client import MQTTMessage

from core.mqtt import Command


class IMQTTClient(Protocol):
    def publish(self, topic: str, payload: str, qos: int = 1) -> None: ...
    @staticmethod
    def create_payload(command: Command, value: Any) -> str: ...
    @staticmethod
    def get_device_publish_topic(device: Any) -> str: ...

class IMessageHandler(Protocol):
    async def handle_message(self, msg: MQTTMessage) -> None: ...