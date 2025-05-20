import json
import random
import time
import os
from datetime import datetime
from paho.mqtt.client import Client
from dateutil.relativedelta import relativedelta
from enum import Enum


MQTT_BROKER = os.getenv("MQTT_BROKER", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
MQTT_USER = os.getenv("MQTT_USER", "localhost")
MQTT_PASS = os.getenv("MQTT_PASS", 0000)

PUBLISH_TOPIC = "devices/lamp-post-1"
CONTROL_TOPIC = "devices/lamp-post-1/control"

class Command(Enum):
    SET_DIMMING = 'set_dimming'

current_state = {
    "dimming_level": 50
}

def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT Broker with result code {rc}")
    client.subscribe(CONTROL_TOPIC)

def on_message(client, userdata, msg):
    global current_state
    try:
        payload = msg.payload.decode()
        command = json.loads(payload)
        print(f"[{datetime.now().isoformat()}] Received command: {command}")

        if command.get("action") == Command.SET_DIMMING.value:
            new_level = int(command.get("value"))

            if 0 <= new_level <= 100:
                current_state["dimming_level"] = new_level
                print(f"Dimming level set to {new_level}%")
            else:
                print("Invalid dimming level")

    except Exception as e:
        print(f"Error processing command: {e}")

def main():
    client = Client()
    client.username_pw_set(MQTT_USER, MQTT_PASS)
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_start()

    try:
        data = []
        with open('data.json') as f:
            data = json.load(f)

        for hour_data in data:
            payload = json.dumps(hour_data)

            addited_payload = {**payload, "dimming_level": current_state["dimming_level"], "lamp_power":current_state["dimming_level"] * 1.5 }

            client.publish(PUBLISH_TOPIC, addited_payload)
            print(f"[{datetime.now().isoformat()}] Published to {PUBLISH_TOPIC}: {payload} \n")
            time.sleep(5)
    except KeyboardInterrupt:
        client.disconnect()
        print("Disconnected from broker.")

if __name__ == "__main__":
    main()