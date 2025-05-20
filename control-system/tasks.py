from celery import Celery
from models import DeviceData
from dim_calculating import calculate_dim_level
import logging
from models import DeviceData
from database import SessionLocal
from mqtt.utils import Command, create_mqtt_payload
from mqtt.settings import get_publish_topic
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

REDIS_HOST = os.getenv("REDIS_HOST", 'localhost')
REDIS_PORT = os.getenv("REDIS_PORT", "6379")

CELERY_BROKER_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}/0'

celery = Celery('tasks', broker=CELERY_BROKER_URL)
def save_device_to_db(data):
    try:
        db = SessionLocal()
        device = DeviceData(**data)
        db.add(device)
        db.commit()
        db.close()
        logger.info(f"Data saved: {data}")
    except Exception as e:
        logger.error(f"Error saving to DB: {e}")

@celery.task
def handle_device_message(device, publish_fn):
    calculated_dim_level = round(calculate_dim_level(device))
    payload = create_mqtt_payload(Command.SET_DIMMING.value, calculated_dim_level)
    publish_fn(get_publish_topic(device["serial_number"]), payload)

    data_to_saving = {**device, "dimming_level": calculated_dim_level}
    save_device_to_db(data_to_saving)