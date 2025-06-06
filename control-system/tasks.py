from typing import Callable
from celery_app import celery_app
from models import DeviceData, DeviceDataCalculatedDim, DeviceDataDict
from dim_calculating import calculate_dim_level
from models import DeviceData
from database import SessionLocal
from mqtt.utils import Command, create_mqtt_payload, DeviceDataMessage
from mqtt.settings import get_publish_topic
from ai_model import device_data_to_model_data, predict_dimming
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def save_device_data_to_db(data):
    logger.info(data)
    try:
        db = SessionLocal()
        device = DeviceData(**data)
        db.add(device)
        db.commit()
        db.refresh(device)
        db.close()
        logger.info(f"Data saved: {data}")
        return device
    except Exception as e:
        logger.error(f"Error saving to DB: {e}")

def save_device_data_calculated_dim_to_db(data):
    try:
        db = SessionLocal()
        device_data_calculated_dim = DeviceDataCalculatedDim(**data)
        db.add(device_data_calculated_dim)
        db.commit()
        db.refresh(device_data_calculated_dim)
        db.close()
        logger.info(f"Data saved: {data}")
        return device_data_calculated_dim
    except Exception as e:
        logger.error(f"Error saving to DB: {e}")

@celery_app.task
def save_calculated_dim_to_db(device_data_id: int, dim_level: int): 
    save_device_data_calculated_dim_to_db({"device_data_id": device_data_id, "dimming_level": dim_level})

@celery_app.task
def process_device_data_dim_level(device_data: DeviceDataDict, publish_fn: Callable[[str, str], None]):
    if device_data['control_type'] == 'simple_rules':
        calculated_dim_level = calculate_dim_level(device_data)
    elif device_data['control_type'] == 'ai_model':
        model_data = device_data_to_model_data(device_data)
        calculated_dim_level = predict_dimming(model_data)
    else:
        raise ValueError(
            f"Invalid control_type: {device_data['control_type']}. "
        )

    payload = create_mqtt_payload(Command.SET_DIMMING.value, calculated_dim_level)
    publish_fn(get_publish_topic(device_data["serial_number"]), payload)
    save_calculated_dim_to_db(device_data["id"], calculated_dim_level)

@celery_app.task
def handle_mqtt_device_data_message(device_data: DeviceDataMessage, publish_fn: Callable[[str, str], None]):
    new_device_data = save_device_data_to_db(device_data)
    process_device_data_dim_level(new_device_data.__dict__, publish_fn)
