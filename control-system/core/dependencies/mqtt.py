from services.mqtt.client import MQTTClient


def get_mqtt_client() -> MQTTClient:
    return MQTTClient()
