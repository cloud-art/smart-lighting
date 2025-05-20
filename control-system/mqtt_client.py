import json
from paho.mqtt.client import Client
from models import DeviceData
from database import SessionLocal
import asyncio
import os
from dotenv import load_dotenv
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

MQTT_BROKER = os.getenv("MQTT_BROKER", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
MQTT_USER = os.getenv("MQTT_USER", "default_user")
MQTT_PASS = os.getenv("MQTT_PASS", "0000")

TOPIC = "devices/#"

def map_device_data(device):
    mapped_device = device

    if "timestamp" in device:
        formatted_datetime = datetime.fromisoformat(device["timestamp"])
        mapped_device["timestamp"] = formatted_datetime

    if "serial_number" in device:
        mapped_device["serial_number"] = int(device["serial_number"])
    
    if "car_count" in device:
        mapped_device["car_count"] = int(device["car_count"])
    
    if "pedestrian_count" in device:
        mapped_device["pedestrian_count"] = int(device["pedestrian_count"])

    return mapped_device

class MQTTClient:
    def __init__(self):
        self.client = Client()
        self._loop = None

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            logger.info("Connected to MQTT Broker!")
            client.subscribe(TOPIC)
        else:
            logger.error(f"Connection failed with code {rc}")

    async def save_to_db(self, data):
        try:
            async with SessionLocal() as session:
                device = DeviceData(**data)
                session.add(device)
                await session.commit()
                logger.info(f"Data saved: {data}")
        except Exception as e:
            logger.error(f"Error saving to DB: {e}")

    def on_message(self, client, userdata, msg):
        try:
            logger.info(f"Message received on {msg.topic}")

            data = json.loads(msg.payload.decode())
            formatted_data = map_device_data(data)

            logger.info(f"Message content: {formatted_data}")
            asyncio.run_coroutine_threadsafe(self.save_to_db(formatted_data), self._loop)
        except Exception as e:
            logger.error(f"Error processing message: {e}")

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