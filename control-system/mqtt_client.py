import json
from paho.mqtt.client import Client
from models import DeviceData
from database import SessionLocal
import asyncio
import os
from dotenv import load_dotenv
import threading
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

MQTT_BROKER = os.getenv("MQTT_BROKER", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
MQTT_USER = os.getenv("MQTT_USER", "default_user")
MQTT_PASS = os.getenv("MQTT_PASS", "0000")

TOPIC = "devices/#"

class MQTTClient:
    def __init__(self):
        self.client = Client()
        self.loop = asyncio.new_event_loop()
        self.thread = None
        self._running = False

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            logger.info("Connected to MQTT Broker!")
            client.subscribe(TOPIC)
            logger.info(f"Subscribed to topic: {TOPIC}")
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
            logger.info(f"Message content: {data}")
            
            if not self.loop.is_running():
                logger.error("Event loop is not running!")
                return
                
            asyncio.run_coroutine_threadsafe(
                self.save_to_db(data),
                self.loop
            )
        except Exception as e:
            logger.error(f"Error processing message: {e}")

    def start_loop(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()

    def start(self):
        try:
            self.thread = threading.Thread(
                target=self.start_loop,
                daemon=True,
                name="MQTT-EventLoop"
            )
            self.thread.start()
            
            while not self.loop.is_running():
                pass

            self.client.on_connect = self.on_connect
            self.client.on_message = self.on_message
            self.client.username_pw_set(MQTT_USER, MQTT_PASS)
            
            logger.info(f"Connecting to {MQTT_BROKER}:{MQTT_PORT}...")
            self.client.connect(MQTT_BROKER, MQTT_PORT, 60)
            self.client.loop_start()
            self._running = True
            logger.info("MQTT client started successfully")
        except Exception as e:
            logger.error(f"Failed to start MQTT client: {e}")
            self.stop()

    def stop(self):
        if self._running:
            self.client.loop_stop()
            self.client.disconnect()
            self.loop.call_soon_threadsafe(self.loop.stop)
            self._running = False
            logger.info("MQTT client stopped")

mqtt_client = MQTTClient()

def start():
    mqtt_client.start()