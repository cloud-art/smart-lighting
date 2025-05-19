import json
import random
import time
import os
from datetime import datetime
from paho.mqtt.client import Client

MQTT_BROKER = os.getenv("MQTT_BROKER", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
MQTT_USER = os.getenv("MQTT_USER", "localhost")
MQTT_PASS = os.getenv("MQTT_PASS", 0000)

TOPIC = "devices/lamp-post-1"

client = Client()
client.username_pw_set(MQTT_USER, MQTT_PASS)
client.connect(MQTT_BROKER, MQTT_PORT, 60)

def generate_device_data():
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "latitude": round(random.uniform(55.0, 55.1), 6),
        "longitude": round(random.uniform(37.5, 37.6), 6),
        "car_count": random.randint(0, 20),
        "car_speed": round(random.uniform(10.0, 60.0), 1),
        "car_density": round(random.uniform(0.1, 1.0), 2),
        "pedestrian_count": random.randint(0, 10),
        "pedestrian_density": round(random.uniform(0.0, 0.5), 2),
        "road_luminance": round(random.uniform(10.0, 100.0), 1),
        "dimming_level": round(random.uniform(0.0, 1.0), 2),
        "lighting_class": random.choice(["A", "B", "C"]),
        "lamp_power": random.choice([30.0, 50.0, 70.0, 100.0])
    }

try:
    while True:
        data = generate_device_data()
        payload = json.dumps(data)
        client.publish(TOPIC, payload)
        print(f"[{datetime.utcnow()}] Published to {TOPIC}: {payload} \n")
        time.sleep(5)
except KeyboardInterrupt:
    client.disconnect()
    print("Disconnected from broker.")
