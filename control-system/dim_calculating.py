from enum import Enum
import logging

from models import DeviceDataDict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Weather(Enum):
    CLEAR = 'clear'
    CLOUDS = "clouds"
    RAIN = 'rain'
    FOG = 'fog'

class LightingClass(Enum):
    A1 = 'A1'
    B1 = 'B1'
    C1 = 'C1'
    D1 = 'D1'

class MovementIntensity:
    NULL = 0
    LOW = 0.40
    MEDIUM = 0.65
    HIGH = 0.85
    FULL = 1

class DimmingLevel(Enum):
    DISABLED = 0
    LOW = 20
    PRE_MEDIUM = 35
    MEDIUM = 50
    PRE_HIGH = 70
    HIGH = 85
    MAXIMUM = 100

def compare_dimming_with_multiplier(multiplier: float) -> DimmingLevel:
    target = multiplier * 100
    closest_level = DimmingLevel.LOW
    min_diff = 100
    
    for level in DimmingLevel:
        diff = abs(level.value - target)
        if diff < min_diff:
            min_diff = diff
            closest_level = level
    
    return closest_level


def calculate_dim_level(device: DeviceDataDict) -> int:
    dimming_multiplier = 0
    ambient_light = device["ambient_light"]
    traffic_density = device["traffic_density"]
    pedestrian_density = device["pedestrian_density"]
    weather = device["pedestrian_density"]

    movement_intensity_multiplier = max(traffic_density, pedestrian_density) 

    if ambient_light > 10000:
        dimming_level = compare_dimming_with_multiplier(dimming_multiplier)
        return dimming_level.value

    if 10000 <= ambient_light <= 6000:
        dimming_multiplier += 0.1
    else:
        dimming_multiplier += 0.2 
    
    if (MovementIntensity.NULL < movement_intensity_multiplier <= MovementIntensity.LOW):
        dimming_multiplier += 0.1
    elif (MovementIntensity.LOW < movement_intensity_multiplier <= MovementIntensity.MEDIUM):
        dimming_multiplier += 0.25
    elif (MovementIntensity.MEDIUM < movement_intensity_multiplier <= MovementIntensity.HIGH):
        dimming_multiplier += 0.5
    elif (MovementIntensity.HIGH < movement_intensity_multiplier <= MovementIntensity.FULL):
        dimming_multiplier += 0.75

    if (weather == Weather.CLOUDS):
        dimming_multiplier += 0.1
    if (weather == Weather.RAIN):
        dimming_multiplier += 0.2
    if (weather == Weather.FOG):
        dimming_multiplier += 0.5

    dimming_level = compare_dimming_with_multiplier(dimming_multiplier)
    return dimming_level.value