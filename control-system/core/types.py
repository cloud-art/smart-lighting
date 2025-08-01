from enum import Enum
from typing import Literal

LightingClass = Literal["A1", "B1", "C1", "D1"]

Weather = Literal["clear", "rain", "clouds", "fog"]

ControlType = Literal["simple_rules", "ai_model"]


class SQLExtractFields(Enum):
    Hour = "hour"
    Day = "day"
    Weekday = "dow"
