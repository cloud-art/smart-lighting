from datetime import datetime
from typing import Dict


def get_time_features(dt: datetime) -> Dict[str, int]:
    day_of_week = dt.weekday()
    return {
        "hour": dt.hour,
        "day_of_week": day_of_week,
        "is_weekend": 1 if day_of_week in [5, 6] else 0,
    }


def format_dow_number(dow_str: str | int):
    weekdays = ['Monday', 'Tuesday', 'Wednesday', 
                'Thursday', 'Friday', 'Saturday', 'Sunday']
    try:
        day_num = int(dow_str)
        return weekdays[day_num]
    except (ValueError, IndexError) as e:
        raise ValueError(f"Invalid day of week value: {dow_str}. Must be 0-6.") from e
