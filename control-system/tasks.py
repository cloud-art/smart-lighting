from celery import Celery
from models import DeviceData
from dim_calculating import calculate_dim_level
import asyncio
import logging
from models import DeviceData
from database import SessionLocal
from mqtt_client import Command, mqtt_client
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

REDIS_HOST = os.getenv("REDIS_HOST", 'localhost')
REDIS_PORT = os.getenv("REDIS_PORT", "6379")

CELERY_BROKER_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}/0'

celery = Celery('tasks', broker=CELERY_BROKER_URL)

async def save_device_to_db(data):
    try:
        async with SessionLocal() as session:
            device = DeviceData(**data)
            session.add(device)
            await session.commit()
            logger.info(f"Data saved: {data}")
    except Exception as e:
        logger.error(f"Error saving to DB: {e}")

@celery.task
def handle_device_message(device):
    calculated_dim_level = round(calculate_dim_level(device))
    payload = mqtt_client.create_mqtt_payload(Command.SET_DIMMING.value, calculated_dim_level)
    mqtt_client.publish("devices/lamp-post-1/control", payload)

    data_to_saving = {**device, "dimming_level": calculated_dim_level}
    asyncio.run_coroutine_threadsafe(save_device_to_db(data_to_saving))
    pass