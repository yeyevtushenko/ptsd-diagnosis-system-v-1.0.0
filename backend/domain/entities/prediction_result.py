from dataclasses import dataclass, field
from typing import Dict, Any


@dataclass
class PredictionResult:
    predicted_class: int

    probability: float
    probability_class_1: float
    probability_class_0: float
    predicted_probability: float

    z: float
    threshold: float

    intercept: float

    feature_contributions: Dict[str, float] = field(default_factory=dict)

    def as_dict(self) -> Dict[str, Any]:
        return {
            "z": self.z,

            "probability": self.probability,

            "probability_class_1": self.probability_class_1,
            "probability_class_0": self.probability_class_0,
            "predicted_probability": self.predicted_probability,

            "predicted_class": self.predicted_class,

            "threshold": self.threshold,
            "intercept": self.intercept,

            "feature_contributions": dict(self.feature_contributions),
        }