from datetime import datetime
import os
import joblib
import pandas as pd

MODEL_FILENAME = os.getenv("MODEL_FILENAME", "model.joblib")

loaded = joblib.load(MODEL_FILENAME)
preprocessor = loaded['preprocessor']
model = loaded['model']

def device_data_to_model_data(device_data):
    timestamp = device_data['timestamp']
    dt = datetime.fromisoformat(timestamp)
    hour = dt.hour
    day_of_week = dt.dayofweek
    is_weekend = day_of_week.isin([5, 6]).astype(int)
    sample_data = dict(hour, day_of_week, is_weekend, **device_data)
    return sample_data

def predict_dimming(sample_data):
    sample_df = pd.DataFrame([sample_data])
    processed_data = preprocessor.transform(sample_df)
    
    prediction = model.predict(processed_data)[0][0]
    return max(0, min(100, prediction))
