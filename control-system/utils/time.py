from datetime import datetime
from typing import Dict

import pandas as pd


def get_time_features(dt: datetime) -> Dict[str, int]:
    day_of_week = dt.weekday()
    return {
        "hour": dt.hour,
        "day_of_week": day_of_week,
        "is_weekend": 1 if day_of_week in [5, 6] else 0,
    }
