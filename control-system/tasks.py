from celery_app import celery_app
from models import DeviceData, DeviceDataCalculatedDim
from dim_calculating import calculate_dim_level
import logging
from models import DeviceData
from database import SessionLocal
from mqtt.utils import Command, create_mqtt_payload
from mqtt.settings import get_publish_topic
from models import ControlType
from ai_model import device_data_to_model_data, predict_dimming

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def save_device_data_to_db(data):
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
def save_calculated_dim_to_db(device_data_id, dim_level): 
    save_device_data_calculated_dim_to_db({"device_data_id": device_data_id, "dimming_level": dim_level})

@celery_app.task
def process_device_data_dim_level(device_data, publish_fn):
    if device_data['control_type'] == ControlType.SIMPLE_RULES.value:
        calculated_dim_level = round(calculate_dim_level(device_data))
    else:
        model_data = device_data_to_model_data(device_data)
        calculated_dim_level = predict_dimming(model_data)

    payload = create_mqtt_payload(Command.SET_DIMMING.value, calculated_dim_level)
    publish_fn(get_publish_topic(device_data["serial_number"]), payload)
    save_calculated_dim_to_db(device_data["id"], calculated_dim_level)

@celery_app.task
def handle_mqtt_device_data_message(device_data, publish_fn):
    new_device_data = save_device_data_to_db(device_data)
    process_device_data_dim_level(new_device_data.__dict__, publish_fn)
