import json
from paho.mqtt.client import MQTTMessage
from datetime import datetime
from mqtt.settings import Command

def create_mqtt_payload(action: Command, value):
    payload = {"action": action, "value": value}
    return json.dumps(payload)

def get_mqtt_device_from_message(msg: MQTTMessage):
    device = json.loads(msg.payload.decode())

    if "timestamp" in device:
        formatted_datetime = datetime.fromisoformat(device["timestamp"])
        device["timestamp"] = formatted_datetime

    if "serial_number" in device:
        device["serial_number"] = int(device["serial_number"])
    
    if "car_count" in device:
        device["car_count"] = int(device["car_count"])
    
    if "pedestrian_count" in device:
        device["pedestrian_count"] = int(device["pedestrian_count"])

    return device