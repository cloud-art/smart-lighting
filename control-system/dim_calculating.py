from models import DeviceData
from enum import Enum

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

def calculate_dim_level(device: DeviceData) -> int:
    print('calucalte_dim_level')
    print(device)
    return 2