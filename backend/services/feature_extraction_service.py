from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Dict, Any

import pandas as pd

from utils.statistics import compute_statistic


class FeatureExtractionService:
    def __init__(self, feature_config_path: str | Path):
        self.feature_config_path = Path(feature_config_path)
        self.feature_config = self._load_feature_config()

    def _load_feature_config(self) -> Dict[str, Any]:
        if not self.feature_config_path.exists():
            raise FileNotFoundError(
                f"Feature config file not found: {self.feature_config_path}"
            )

        with open(self.feature_config_path, "r", encoding="utf-8") as file:
            config = json.load(file)

        if "features" not in config:
            raise ValueError("Feature config must contain a 'features' key.")

        return config

    def _normalize_name(self, name: str) -> str:

        name = name.strip()
        name = re.sub(r"\s*->\s*", " -> ", name)
        name = re.sub(r"\s+", " ", name)
        return name

    def extract_from_csv(self, csv_path: str | Path) -> Dict[str, float]:

        csv_path = Path(csv_path)

        if not csv_path.exists():
            raise FileNotFoundError(f"Patient CSV file not found: {csv_path}")

        df = pd.read_csv(csv_path)

        df.columns = [self._normalize_name(col) for col in df.columns]

        extracted_features: Dict[str, float] = {}
        missing_roi_pairs = []

        for feature in self.feature_config["features"]:
            if not feature.get("enabled", True):
                continue

            feature_name = feature["name"]
            roi_pair = self._normalize_name(feature["roi_pair"])
            stat_name = feature["stat"]

            if roi_pair not in df.columns:
                missing_roi_pairs.append(roi_pair)
                continue

            signal = df[roi_pair].values

            try:
                value = compute_statistic(signal, stat_name)
            except Exception as e:
                raise RuntimeError(
                    f"Error computing '{stat_name}' for feature '{feature_name}' "
                    f"(ROI: {roi_pair}): {e}"
                )

            extracted_features[feature_name] = float(value)

        if missing_roi_pairs:
            missing_text = "\n".join(missing_roi_pairs)
            raise ValueError(
                "The following ROI pairs were not found in the patient's CSV file:\n"
                f"{missing_text}"
            )

        return dict(
            sorted(
                extracted_features.items(),
                key=lambda item: int(item[0][1:])
            )
        )

    def extract_from_dataframe(self, df: pd.DataFrame) -> Dict[str, float]:

        df.columns = [self._normalize_name(col) for col in df.columns]

        extracted_features: Dict[str, float] = {}
        missing_roi_pairs = []

        for feature in self.feature_config["features"]:
            if not feature.get("enabled", True):
                continue

            feature_name = feature["name"]
            roi_pair = self._normalize_name(feature["roi_pair"])
            stat_name = feature["stat"]

            if roi_pair not in df.columns:
                missing_roi_pairs.append(roi_pair)
                continue

            signal = df[roi_pair].values

            try:
                value = compute_statistic(signal, stat_name)
            except Exception as e:
                raise RuntimeError(
                    f"Error computing '{stat_name}' for feature '{feature_name}' "
                    f"(ROI: {roi_pair}): {e}"
                )

            extracted_features[feature_name] = float(value)

        if missing_roi_pairs:
            missing_text = "\n".join(missing_roi_pairs)
            raise ValueError(
                "The following ROI pairs were not found in the DataFrame:\n"
                f"{missing_text}"
            )

        return dict(
            sorted(
                extracted_features.items(),
                key=lambda item: int(item[0][1:])
            )
        )