from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Dict, Any, List

import pandas as pd


class ValidationService:

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

    def validate_csv(self, csv_path: str | Path) -> Dict[str, Any]:
        csv_path = Path(csv_path)

        errors: List[str] = []
        warnings: List[str] = []

        if not csv_path.exists():
            return {
                "is_valid": False,
                "errors": [f"File not found: {csv_path}"],
                "warnings": [],
                "file_info": {},
            }

        if csv_path.suffix.lower() != ".csv":
            errors.append(f"Invalid file format: expected .csv, got {csv_path.suffix}")

        try:
            df = pd.read_csv(csv_path)
        except Exception as e:
            return {
                "is_valid": False,
                "errors": [f"Failed to read CSV file: {e}"],
                "warnings": [],
                "file_info": {},
            }

        if df.empty:
            errors.append("CSV file is empty.")

        original_column_count = len(df.columns)
        df.columns = [self._normalize_name(col) for col in df.columns]

        required_features = [
            feature for feature in self.feature_config["features"]
            if feature.get("enabled", True)
        ]

        missing_roi_pairs: List[str] = []
        empty_columns: List[str] = []
        non_numeric_columns: List[str] = []

        for feature in required_features:
            roi_pair = self._normalize_name(feature["roi_pair"])

            if roi_pair not in df.columns:
                missing_roi_pairs.append(roi_pair)
                continue

            column = df[roi_pair]

            if column.isna().all():
                empty_columns.append(roi_pair)
                continue

            numeric_column = pd.to_numeric(column, errors="coerce")

            if numeric_column.isna().all():
                non_numeric_columns.append(roi_pair)
                continue

            if numeric_column.isna().any():
                warnings.append(
                    f"Column '{roi_pair}' contains some non-numeric or missing values. "
                    f"They may be ignored during computation."
                )

        if missing_roi_pairs:
            errors.append(
                "Missing required ROI pairs:\n" + "\n".join(missing_roi_pairs)
            )

        if empty_columns:
            errors.append(
                "Columns with only missing values:\n" + "\n".join(empty_columns)
            )

        if non_numeric_columns:
            errors.append(
                "Columns with no numeric values:\n" + "\n".join(non_numeric_columns)
            )

        result = {
            "is_valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
            "file_info": {
                "file_name": csv_path.name,
                "rows": int(df.shape[0]),
                "columns": int(original_column_count),
                "normalized_columns": int(len(df.columns)),
                "required_feature_count": len(required_features),
            },
        }

        return result