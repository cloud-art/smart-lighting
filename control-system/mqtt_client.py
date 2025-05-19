import json
from paho.mqtt.client import Client
from models import DeviceData
from database import SessionLocal
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

MQTT_USER=os.getenv("MQTT_USER", "localhost")
MQTT_PASS=int(os.getenv("MQTT_PASS", 1883))
BROKER = os.getenv("MQTT_BROKER", "localhost")
PORT = int(os.getenv("MQTT_PORT", 1883))
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
    client.username_pw_set("user", "password")
    client.connect(BROKER, PORT, 60)
    client.loop_start()
