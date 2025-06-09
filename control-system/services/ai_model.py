import joblib
import pandas as pd

from core.logger import logger
from schemas.ai_model import ModelInputData
from schemas.device_data import DeviceDataSchema
from utils.time import get_time_features


class AiModel:
    def __init__(self, model_path: str):
        self.model = joblib.load(model_path)

    @staticmethod
    def prepare_data(raw_data: DeviceDataSchema) -> ModelInputData:
        time_features = get_time_features(raw_data.timestamp)

        return ModelInputData(
            **raw_data,
            hour=time_features["hour"],
            day_of_week=time_features["day_of_week"],
            is_weekend=time_features["is_weekend"],
        )

    def predict_dimming(self, model_data: ModelInputData) -> int:
        try:
            data = pd.DataFrame([model_data])
            prediction = self.model.predict(data)[0]
            prediction_int = int(prediction)
            return max(0, min(100, prediction_int))
        except Exception as e:
            logger.error(f"Error predicting: {e}")
