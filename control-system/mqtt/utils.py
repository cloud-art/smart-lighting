import json
from typing import TypedDict, Union
from paho.mqtt.client import MQTTMessage
from datetime import datetime
from common import LightingClass, Weather
from mqtt.settings import Command

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DeviceDataRawMessage(TypedDict):
    timestamp: str
    serial_number: str
    control_type: str
    latitude: str
    longitude: str
    car_count: str
    traffic_speed: str
    traffic_density: str
    pedestrian_count: str
    pedestrian_density: str
    ambient_light: str
    dimming_level: str
    lighting_class: str
    lamp_power: str
    weather: str

class DeviceDataMessage(TypedDict):
    timestamp: datetime
    serial_number: int
    control_type: str
    latitude: float
    longitude: float
    car_count: int
    traffic_speed: float
    traffic_density: float
    pedestrian_count: int
    pedestrian_density: float
    ambient_light: float
    dimming_level: float
    lighting_class: LightingClass
    lamp_power: float
    weather: Weather


def create_mqtt_payload(action: Command, value: Union[str, int, float, bool]):
    payload = {"action": action, "value": value}
    try: 
        json_payload = json.dumps(payload)
        return json_payload
    except Exception as e:
        logger.error(f"Error json serializing: {e}")



def mqtt_raw_device_message_to_device_message(raw_device_message: DeviceDataRawMessage) -> DeviceDataMessage:
    return {**raw_device_message,
                "timestamp": datetime.fromisoformat(raw_device_message["timestamp"]),
                "serial_number": int(raw_device_message["serial_number"]),
                "latitude": float(raw_device_message["latitude"]),
                "longitude": float(raw_device_message["longitude"]),
                "car_count": int(raw_device_message["car_count"]),
                "traffic_speed": float(raw_device_message["traffic_speed"]),
                "traffic_density": float(raw_device_message["traffic_density"]),
                "pedestrian_count": int(raw_device_message["pedestrian_count"]),
                "pedestrian_density": float(raw_device_message["pedestrian_density"]),
                "ambient_light": float(raw_device_message["ambient_light"]),
                "dimming_level": float(raw_device_message["dimming_level"]),
                "lamp_power": float(raw_device_message["lamp_power"]),
            }

def get_mqtt_device_from_message(msg: MQTTMessage) -> DeviceDataMessage:
    raw_device_data: DeviceDataRawMessage = json.loads(msg.payload.decode())
    device_message = mqtt_raw_device_message_to_device_message(raw_device_data)
    return device_message