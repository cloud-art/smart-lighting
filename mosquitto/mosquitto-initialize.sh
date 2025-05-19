#!/bin/sh

USER="$1"
PASS="$2"

if [ ! -f /mosquitto/config/mqttuser ]; then
  mosquitto_passwd -b -c /mosquitto/config/mqttuser "$USER" "$PASS"
fi

if [ -f /mosquitto.conf.temporary ]; then
  cp /mosquitto.conf.temporary /mosquitto/config/mosquitto.conf
  rm /mosquitto.conf.temporary
fi
