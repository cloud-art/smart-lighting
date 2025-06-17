import joblib
import pandas as pd
from sklearn.pipeline import Pipeline

from core.logger import logger
from schemas.ai_model import ModelInputData
from schemas.device_data import DeviceDataSchema
from utils.time import get_time_features


class AiModel:
    def __init__(self, model_path: str):
        self.modela: Pipeline = joblib.load(model_path)

    @staticmethod
    def prepare_data(raw_data: DeviceDataSchema) -> ModelInputData:
        time_features = get_time_features(raw_data.timestamp)

        return ModelInputData(
            car_count=raw_data.car_count,
            traffic_speed=raw_data.traffic_speed,
            traffic_density=raw_data.traffic_density,
            pedestrian_count=raw_data.pedestrian_count,
            pedestrian_density=raw_data.pedestrian_density,
            lighting_class=raw_data.device.lighting_class,
            ambient_light=raw_data.ambient_light,
            weather=raw_data.weather,
            hour=time_features["hour"],
            day_of_week=time_features["day_of_week"],
            is_weekend=time_features["is_weekend"],
        )

    def predict_dimming(self, model_data: ModelInputData) -> int:
        try:
            data = pd.DataFrame([model_data.__dict__])
            prediction = self.modela.predict(data)[0]
            prediction_int = int(prediction)
            return max(0, min(100, prediction_int))
        except Exception as e:
            logger.error(f"Error predicting: {e}")
