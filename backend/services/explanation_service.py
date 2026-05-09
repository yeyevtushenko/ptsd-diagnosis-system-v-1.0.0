from __future__ import annotations

from typing import Dict, Any, List, Tuple


class ExplanationService:
    def __init__(self, top_n: int = 10):
        self.top_n = top_n

    def _sort_absolute(
            self, feature_contributions: Dict[str, float]
    ) -> List[Tuple[str, float]]:
        return sorted(
            feature_contributions.items(),
            key=lambda item: abs(item[1]),
            reverse=True
        )

    def _split_contributions(
            self, feature_contributions: Dict[str, float]
    ) -> tuple[list[tuple[str, float]], list[tuple[str, float]]]:
        positive = sorted(
            [(name, value) for name, value in feature_contributions.items() if value > 0],
            key=lambda item: item[1],
            reverse=True
        )

        negative = sorted(
            [(name, value) for name, value in feature_contributions.items() if value < 0],
            key=lambda item: item[1]
        )

        return positive, negative

    def build_explanation(self, prediction_result: Dict[str, Any]) -> Dict[str, Any]:
        probability = float(prediction_result["probability"])
        predicted_class = int(prediction_result["predicted_class"])
        z_value = float(prediction_result["z"])
        threshold = float(prediction_result["threshold"])
        intercept = float(prediction_result["intercept"])
        feature_contributions = prediction_result["feature_contributions"]

        top_absolute = self._sort_absolute(feature_contributions)[: self.top_n]
        top_positive, top_negative = self._split_contributions(feature_contributions)

        if predicted_class == 1:
            summary = (
                f"Model prediction: class 1 with probability {probability:.4f}. "
                f"The linear score z = {z_value:.4f}, threshold = {threshold:.2f}."
            )
        else:
            summary = (
                f"Model prediction: class 0 with probability {probability:.4f}. "
                f"The linear score z = {z_value:.4f}, threshold = {threshold:.2f}."
            )

        return {
            "summary": summary,
            "predicted_class": predicted_class,
            "probability": probability,
            "z": z_value,
            "threshold": threshold,
            "intercept": intercept,
            "top_absolute_contributions": [
                {"feature": name, "contribution": value}
                for name, value in top_absolute
            ],
            "top_positive_contributions": [
                {"feature": name, "contribution": value}
                for name, value in top_positive[: self.top_n]
            ],
            "top_negative_contributions": [
                {"feature": name, "contribution": value}
                for name, value in top_negative[: self.top_n]
            ],
        }
