from datetime import datetime
import os
from typing import TypedDict
import joblib
import pandas as pd

from common import CONTROL_TYPE
from models import DeviceDataDict

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MODEL_FILENAME = os.getenv("MODEL_FILENAME", "model_xgboost.joblib")

model = joblib.load(MODEL_FILENAME)

class ModelDeviceData(TypedDict): 
    id: int
    timestamp: datetime
    serial_number: int
    control_type: CONTROL_TYPE
    latitude: float
    longitude: float
    car_count: int
    traffic_speed: float
    traffic_density: float
    pedestrian_count: int
    pedestrian_density: float
    ambient_light: float
    dimming_level: float
    lighting_class: str
    lamp_power: float
    weather: str
    hour: int
    day_of_week: int
    is_weekend: int

def device_data_to_model_data(device_data: DeviceDataDict) -> ModelDeviceData:
    dt = pd.to_datetime(device_data['timestamp'])
    hour = dt.hour
    day_of_week = dt.dayofweek
    is_weekend = 1 if day_of_week in [5, 6] else 0
    model_data: ModelDeviceData  = dict({**device_data, "hour": hour, "day_of_week": day_of_week, "is_weekend": is_weekend})
    return model_data

def predict_dimming(model_data: ModelDeviceData) -> int:
    try:
        data = pd.DataFrame([model_data])
        prediction = model.predict(data)[0]
        prediction_int = int(prediction)
        return max(0, min(100, prediction_int))
    except Exception as e:
        logger.error(f"Error predicting: {e}")