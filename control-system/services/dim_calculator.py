from schemas.device_data import DeviceDataSchema
from services.ai_model import AiModel
from utils.dim_calculating import calculate_dim_level


class DimmingCalculator:
    def __init__(self, ai_model: AiModel):
        self.ai_model = ai_model

    def calculate(self, device_data: DeviceDataSchema) -> int:
        control_type = device_data.device.control_type

        if control_type == "simple_rules":
            return self.calculate_simple(device_data)
        elif control_type == "ai_model":
            return self.calculate_ai(device_data)
        else:
            raise ValueError(f"Unsupported control_type: {control_type}")

    def calculate_simple(self, device_data: DeviceDataSchema) -> int:
        dim_level = calculate_dim_level(device_data)
        return dim_level

    def calculate_ai(self, device_data: DeviceDataSchema) -> int:
        model_data = self.ai_model.prepare_data(device_data)
        return self.ai_model.predict_dimming(model_data)
