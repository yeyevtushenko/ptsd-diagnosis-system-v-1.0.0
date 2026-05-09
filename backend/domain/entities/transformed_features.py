from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict

@dataclass
class TransformedFeatures:
    values: Dict[str, float] = field(default_factory=dict)

    def get(self, feature_name: str) -> float:
        return self.values[feature_name]
    def as_dict(self) -> Dict[str, float]:
        return dict(self.values)