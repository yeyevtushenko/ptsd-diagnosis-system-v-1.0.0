from pathlib import Path

import pandas as pd

from backend.services.validation_service import ValidationService


def test_validation_rejects_missing_file():
    service = ValidationService("config/feature_config.json")

    result = service.validate_csv("data/input/not_existing_file.csv")

    assert result["is_valid"] is False
    assert len(result["errors"]) > 0


def test_validation_rejects_non_csv_file(tmp_path):
    test_file = tmp_path / "test.txt"
    test_file.write_text("test content", encoding="utf-8")

    service = ValidationService("config/feature_config.json")

    result = service.validate_csv(test_file)

    assert result["is_valid"] is False
    assert any("Invalid file format" in error for error in result["errors"])


def test_validation_rejects_empty_csv(tmp_path):
    test_file = tmp_path / "empty.csv"
    pd.DataFrame().to_csv(test_file, index=False)

    service = ValidationService("config/feature_config.json")

    result = service.validate_csv(test_file)

    assert result["is_valid"] is False
