import os
import pickle
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from typing import Tuple

# ---------------------- FIXED MODEL PATH ----------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "performance_model.pkl")


# ---------------------- TRAINING FUNCTION ----------------------
def train_performance_model(X: np.ndarray, y: np.ndarray) -> Tuple[RandomForestRegressor, dict]:

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestRegressor(
        n_estimators=100, random_state=42, max_depth=10
    )
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    metrics = {
        "mse": mean_squared_error(y_test, y_pred),
        "r2_score": r2_score(y_test, y_pred)
    }

    return model, metrics


# ---------------------- SAVE MODEL ----------------------
def save_model(model: RandomForestRegressor, filepath: str = MODEL_PATH):

    model_dir = os.path.dirname(filepath)

    if model_dir and not os.path.exists(model_dir):
        os.makedirs(model_dir, exist_ok=True)

    with open(filepath, "wb") as f:
        pickle.dump(model, f)


# ---------------------- LOAD MODEL ----------------------
def load_model(filepath: str = MODEL_PATH):

    if not os.path.exists(filepath):
        return None

    with open(filepath, "rb") as f:
        return pickle.load(f)


# ---------------------- PREDICT PERFORMANCE ----------------------
def predict_performance(model: RandomForestRegressor, features: np.ndarray) -> float:

    if model is None:
        raise ValueError("Model not found. Train or load it before prediction.")

    prediction = model.predict(features)
    return float(prediction[0])


# ---------------------- PREPARE FEATURES ----------------------
def prepare_features(kpi_score: float, attendance_percentage: float) -> np.ndarray:
    return np.array([[kpi_score, attendance_percentage]])
