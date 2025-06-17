from fastapi import Depends

from core.dependencies.service import get_ai_model
from schemas.device_data import DeviceDataSchema
from services.ai_model import AiModel
from utils.dim_calculating import calculate_dim_level


class DimmingCalculator:
    @staticmethod
    def calculate(device_data: DeviceDataSchema) -> int:
        control_type = device_data.device.control_type

        if control_type == "simple_rules":
            return DimmingCalculator._calculate_simple(device_data)
        elif control_type == "ai_model":
            return DimmingCalculator._calculate_ai(device_data)
        else:
            raise ValueError(f"Unsupported control_type: {control_type}")

    @staticmethod
    def _calculate_simple(device_data: DeviceDataSchema) -> int:
        dim_level = calculate_dim_level(device_data)
        return dim_level

    @staticmethod
    def _calculate_ai(
        device_data: DeviceDataSchema, ai_model: AiModel = Depends(get_ai_model())
    ) -> int:
        model_data = ai_model.prepare_data(device_data)
        return ai_model.predict_dimming(model_data)
