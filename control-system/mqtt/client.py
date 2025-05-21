from paho.mqtt.client import Client, MQTTMessage
import asyncio
import os
from dotenv import load_dotenv
import logging
from tasks import handle_mqtt_device_data_message
from mqtt.settings import RECIEVE_TOPIC
from mqtt.utils import get_mqtt_device_from_message

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

MQTT_BROKER = os.getenv("MQTT_BROKER", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
MQTT_USER = os.getenv("MQTT_USER", "default_user")
MQTT_PASS = os.getenv("MQTT_PASS", "0000")

class MQTTClient:
    def __init__(self):
        self.client = Client()
        self._loop = None

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            logger.info("Connected to MQTT Broker!")
            client.subscribe(RECIEVE_TOPIC)
        else:
            logger.error(f"Connection failed with code {rc}")

    def on_message(self, client, userdata, msg: MQTTMessage):
        try:
            logger.info(f"Message received on {msg.topic}")
            data = get_mqtt_device_from_message(msg)
            logger.info(f"Message content: {data}")
            handle_mqtt_device_data_message(data, self.client.publish)
        except Exception as e:
            logger.error(f"Error processing message: {e}")

    def publish(self, topic, payload):
        self.client.publish(topic=topic, payload=payload)

    async def start(self):
        self._loop = asyncio.get_running_loop()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.username_pw_set(MQTT_USER, MQTT_PASS)
        logger.info(f"Connecting to {MQTT_BROKER}:{MQTT_PORT}...")
        self.client.connect(MQTT_BROKER, MQTT_PORT, 60)
        self.client.loop_start()
        logger.info("MQTT client started")


mqtt_client = MQTTClient()

def start():
    mqtt_client.start()