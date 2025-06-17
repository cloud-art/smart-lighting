from enum import Enum

DEVICE_RECIEVE_TOPIC = "devices/+/data"


def get_device_publish_topic(id: str | int):
    return f"devices/{id}/control"


class Command(Enum):
    SET_DIMMING = "set_dimming"
