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

try:
    data = []
    with open('data.json') as f:
        data = json.load(f)

    for hour_data in data:
        payload = json.dumps(hour_data)
        client.publish(TOPIC, payload)
        print(f"[{datetime.now().isoformat()}] Published to {TOPIC}: {payload} \n")
        time.sleep(5)
except KeyboardInterrupt:
    client.disconnect()
    print("Disconnected from broker.")
