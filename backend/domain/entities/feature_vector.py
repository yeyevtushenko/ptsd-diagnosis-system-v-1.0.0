from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict

@dataclass
class FeatureVector:
    value: Dict[str, float] = field(default_factory=dict)

    def get(self, feature_name: str) -> float:
        return self.value[feature_name]

    def as_dict(self) -> Dict[str, float]:
        return dict(self.value)
