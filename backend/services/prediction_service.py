from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Dict, Any


class PredictionService:
    def __init__(self, model_coefficients_path: str | Path, threshold: float = 0.5):
        self.model_coefficients_path = Path(model_coefficients_path)
        self.threshold = threshold
        self.model_config = self._load_model_coefficients()

    def _load_model_coefficients(self) -> Dict[str, Any]:
        if not self.model_coefficients_path.exists():
            raise FileNotFoundError(
                f"Model coefficients file not found: {self.model_coefficients_path}"
            )

        with open(self.model_coefficients_path, "r", encoding="utf-8") as file:
            config = json.load(file)

        if "intercept" not in config:
            raise ValueError("model_coefficients.json must contain 'intercept'.")
        if "coefficients" not in config:
            raise ValueError("model_coefficients.json must contain 'coefficients'.")

        return config

    def _sigmoid(self, z: float) -> float:
        if z >= 0:
            return 1.0 / (1.0 + math.exp(-z))
        exp_z = math.exp(z)
        return exp_z / (1.0 + exp_z)

    def predict(self, transformed_features: Dict[str, float]) -> Dict[str, Any]:
        intercept = float(self.model_config["intercept"])
        coefficients: Dict[str, float] = self.model_config["coefficients"]

        missing_features = [
            feature_name
            for feature_name in coefficients.keys()
            if feature_name not in transformed_features
        ]

        if missing_features:
            missing_text = ", ".join(missing_features)
            raise ValueError(
                f"Missing transformed features required for prediction: {missing_text}"
            )

        z = intercept
        feature_contributions: Dict[str, float] = {}

        for feature_name, coefficient in coefficients.items():
            coef_value = float(coefficient)
            feature_value = float(transformed_features[feature_name])

            contribution = coef_value * feature_value
            feature_contributions[feature_name] = contribution
            z += contribution

        probability = self._sigmoid(z)
        predicted_class = 1 if probability >= self.threshold else 0

        probability_class_1 = probability
        probability_class_0 = 1.0 - probability_class_1

        predicted_probability = (probability_class_1 if predicted_class == 1 else probability_class_0)

        return {
            "z": float(z),
            "probability": float(probability),
            "probability_class_1": float(probability_class_1),
            "probability_class_0": float(probability_class_0),
            "predicted_probability": float(predicted_probability),
            "predicted_class": int(predicted_class),
            "threshold": float(self.threshold),
            "intercept": float(intercept),
            "feature_contributions": feature_contributions,
        }