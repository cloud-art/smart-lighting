from enum import Enum

RECIEVE_TOPIC = "devices/+/data"

def get_publish_topic(device):
    return f"devices/{device}/control"

class Command(Enum):
    SET_DIMMING = 'set_dimming'
