from datetime import datetime
import os
import joblib
import pandas as pd

MODEL_FILENAME = os.getenv("MODEL_FILENAME", "model_xgboost.joblib")

model = joblib.load(MODEL_FILENAME)

def device_data_to_model_data(device_data):
    timestamp = device_data['timestamp']
    dt = pd.to_datetime(timestamp)
    hour = dt.hour
    day_of_week = dt.dayofweek
    is_weekend = 1 if day_of_week in [5, 6] else 0
    sample_data = dict({"hour": hour, "day_of_week": day_of_week, "is_weekend": is_weekend, **device_data})
    return sample_data

def predict_dimming(sample_data):
    data = pd.DataFrame([sample_data])
    prediction = model.predict(data)[0]
    return max(0, min(100, prediction))
