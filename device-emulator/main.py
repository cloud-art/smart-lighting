import json
import random
import time
import os
from datetime import datetime
from paho.mqtt.client import Client
from dateutil.relativedelta import relativedelta

MQTT_BROKER = os.getenv("MQTT_BROKER", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
MQTT_USER = os.getenv("MQTT_USER", "localhost")
MQTT_PASS = os.getenv("MQTT_PASS", 0000)

TOPIC = "devices/lamp-post-1"

client = Client()
client.username_pw_set(MQTT_USER, MQTT_PASS)
client.connect(MQTT_BROKER, MQTT_PORT, 60)

import random
import time
import json
from datetime import datetime
import paho.mqtt.client as mqtt

BROKER = "localhost"
TOPIC = "devices/lamp-1"

LAMP_ID = "lamp_1"
COORDINATES = (47.224860, 39.702285)
LIGHTING_CLASS = "A1"
START_DATETIME = datetime.now() - relativedelta(months=6)
DEFAULT_DIMMING = 1

CALCULATING_DATE

def generate_data():
    now = datetime.now()
    hour = now.hour

    if 6 <= hour <= 18:
        illuminance = random.uniform(1000, 10000)  # день
    else:
        illuminance = random.uniform(0, 200)       # ночь

    if 7 <= hour <= 9 or 17 <= hour <= 19:
        cars = random.randint(40, 80)  # час пик
        peds = random.randint(10, 30)
    elif 0 <= hour <= 5:
        cars = random.randint(0, 10)
        peds = random.randint(0, 5)
    else:
        cars = random.randint(10, 40)
        peds = random.randint(5, 20)

    speed = random.uniform(10, 60) if cars > 0 else 0
    traffic_density = min(cars / 100, 1.0)
    pedestrian_density = min(peds / 50, 1.0)

    power = DEFAULT_DIMMING * 100

    return {
        "timestamp": now.isoformat(),
        "lamp_id": LAMP_ID,
        "coordinates": {"lat": COORDINATES[0], "lon": COORDINATES[1]},
        "car_count": cars,
        "traffic_speed": round(speed, 2),
        "traffic_density": round(traffic_density, 2),
        "pedestrian_count": peds,
        "pedestrian_density": round(pedestrian_density, 2),
        "illuminance": round(illuminance, 2),
        "dimming_level": DEFAULT_DIMMING,
        "lighting_class": LIGHTING_CLASS,
        "lamp_power": power
    }

try:
    while True:
        data = generate_data()
        payload = json.dumps(data)
        client.publish(TOPIC, payload)
        print(f"[{datetime.utcnow()}] Published to {TOPIC}: {payload} \n")
        time.sleep(5)
except KeyboardInterrupt:
    client.disconnect()
    print("Disconnected from broker.")
