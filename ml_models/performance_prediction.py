import pickle
import os
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from typing import List, Tuple

MODEL_PATH = "ml_models/performance_model.pkl"

def train_performance_model(X: np.ndarray, y: np.ndarray) -> Tuple[RandomForestRegressor, dict]:
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestRegressor(n_estimators=100, random_state=42, max_depth=10)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    metrics = {
        "mse": mean_squared_error(y_test, y_pred),
        "r2_score": r2_score(y_test, y_pred)
    }

    return model, metrics

def save_model(model: RandomForestRegressor, filepath: str = MODEL_PATH):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'wb') as f:
        pickle.dump(model, f)

def load_model(filepath: str = MODEL_PATH) -> RandomForestRegressor:
    if not os.path.exists(filepath):
        return None
    with open(filepath, 'rb') as f:
        return pickle.load(f)

def predict_performance(model: RandomForestRegressor, features: np.ndarray) -> float:
    prediction = model.predict(features)
    return float(prediction[0])

def prepare_features(kpi_score: float, attendance_percentage: float) -> np.ndarray:
    return np.array([[kpi_score, attendance_percentage]])
