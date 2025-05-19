import json
from paho.mqtt.client import Client
from models import DeviceData
from database import SessionLocal
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

MQTT_BROKER = os.getenv("MQTT_BROKER", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
MQTT_USER = os.getenv("MQTT_USER", "default_user")
MQTT_PASS = os.getenv("MQTT_PASS", 0000)

TOPIC = "devices/#"

client = Client()

def on_connect(client, userdata, flags, rc):
    print("Connected with result code", rc)
    client.subscribe(TOPIC)

def on_message(client, userdata, msg):
    loop = asyncio.get_event_loop()
    data = json.loads(msg.payload.decode())
    loop.create_task(save_to_db(data))

async def save_to_db(data):
    async with SessionLocal() as session:
        device = DeviceData(**data)
        session.add(device)
        await session.commit()

def start():
    client.on_connect = on_connect
    client.on_message = on_message
    client.username_pw_set(MQTT_USER, MQTT_PASS)
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_start()
