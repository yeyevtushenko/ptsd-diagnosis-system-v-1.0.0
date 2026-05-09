from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Dict, Any

EPSILON = 1e-8


class FeatureTransformationService:
    def __init__(
            self,
            selected_features_path: str | Path,
            model_coefficients_path: str | Path,
    ):
        self.selected_features_path = Path(selected_features_path)
        self.model_coefficients_path = Path(model_coefficients_path)

        self.selected_features_config = self._load_json(self.selected_features_path)
        self.model_coefficients_config = self._load_json(self.model_coefficients_path)

    def _load_json(self, path: Path) -> Dict[str, Any]:
        if not path.exists():
            raise FileNotFoundError(f"JSON file not found: {path}")

        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)

    def _get_selected_base_features(self) -> list[str]:
        if "base_features" not in self.selected_features_config:
            raise ValueError(
                "selected_features.json must contain a 'base_features' key."
            )
        return self.selected_features_config["base_features"]

    def _get_model_expressions(self) -> list[str]:
        if "coefficients" not in self.model_coefficients_config:
            raise ValueError(
                "model_coefficients.json must contain a 'coefficients' key."
            )
        return list(self.model_coefficients_config["coefficients"].keys())

    def _validate_base_features(self, base_features: Dict[str, float]) -> None:
        selected_base_features = self._get_selected_base_features()
        missing = [name for name in selected_base_features if name not in base_features]

        if missing:
            missing_text = ", ".join(missing)
            raise ValueError(
                f"Missing required base features for transformation: {missing_text}"
            )

    def _evaluate_expression(
            self,
            expression: str,
            base_features: Dict[str, float],
    ) -> float:

        expression = expression.strip()

        if re.fullmatch(r"x\d+", expression):
            if expression not in base_features:
                raise ValueError(f"Base feature '{expression}' not found.")
            return float(base_features[expression])

        power_match = re.fullmatch(r"(x\d+)\^(\d+)", expression)
        if power_match:
            feature_name, power = power_match.groups()
            if feature_name not in base_features:
                raise ValueError(f"Base feature '{feature_name}' not found.")
            return float(base_features[feature_name] ** int(power))

        binary_match = re.fullmatch(r"(x\d+)\s*([\*/])\s*(x\d+)", expression)
        if binary_match:
            left_name, operator, right_name = binary_match.groups()

            if left_name not in base_features:
                raise ValueError(f"Base feature '{left_name}' not found.")
            if right_name not in base_features:
                raise ValueError(f"Base feature '{right_name}' not found.")

            left_value = float(base_features[left_name])
            right_value = float(base_features[right_name])

            if operator == "*":
                return float(left_value * right_value)

            if operator == "/":
                if abs(right_value) < 1e-6:
                    return 0.0
                return left_value / right_value

        raise ValueError(f"Unsupported expression format: '{expression}'")

    def transform(self, base_features: Dict[str, float]) -> Dict[str, float]:
        self._validate_base_features(base_features)

        model_expressions = self._get_model_expressions()
        transformed_features: Dict[str, float] = {}

        for expression in model_expressions:
            transformed_features[expression] = self._evaluate_expression(
                expression=expression,
                base_features=base_features,
            )

        return transformed_features
