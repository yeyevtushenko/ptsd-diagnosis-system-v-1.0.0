from __future__ import annotations

from pathlib import Path
from typing import Dict, Any

from config.paths import (
    FEATURE_CONFIG_PATH,
    SELECTED_FEATURES_PATH,
    MODEL_COEFFICIENTS_PATH
)
from backend.services.validation_service import ValidationService
from backend.services.feature_extraction_service import FeatureExtractionService
from backend.services.feature_transformation_service import FeatureTransformationService
from backend.services.prediction_service import PredictionService
from backend.services.explanation_service import ExplanationService

from backend.domain.entities.patient_record import PatientRecord
from backend.domain.entities.feature_vector import FeatureVector
from backend.domain.entities.transformed_features import TransformedFeatures
from backend.domain.entities.prediction_result import PredictionResult


class AppController:

    def __init__(self):
        self.feature_config_path = FEATURE_CONFIG_PATH
        self.selected_features_path = SELECTED_FEATURES_PATH
        self.model_coefficients_path = MODEL_COEFFICIENTS_PATH

        self.validator = ValidationService(self.feature_config_path)
        self.extractor = FeatureExtractionService(self.feature_config_path)
        self.transformer = FeatureTransformationService(
            self.selected_features_path,
            self.model_coefficients_path
        )
        self.predictor = PredictionService(self.model_coefficients_path)
        self.explainer = ExplanationService(top_n=10)

    def analyze_patient(self, csv_path: str | Path) -> Dict[str, Any]:
        csv_path = Path(csv_path)

        patient = PatientRecord.from_path(csv_path)

        validation_result = self.validator.validate_csv(csv_path)

        if not validation_result["is_valid"]:
            return {
                "status": "error",
                "stage": "validation",
                "errors": validation_result["errors"],
                "warnings": validation_result["warnings"],
                "file_info": validation_result.get("file_info", {})
            }

        try:
            base_features_dict = self.extractor.extract_from_csv(csv_path)
            base_features = FeatureVector(base_features_dict)
        except Exception as e:
            return {
                "status": "error",
                "stage": "feature_extraction",
                "message": str(e)
            }

        try:
            transformed_dict = self.transformer.transform(base_features.as_dict())
            transformed_features = TransformedFeatures(transformed_dict)
        except Exception as e:
            return {
                "status": "error",
                "stage": "feature_transformation",
                "message": str(e)
            }

        try:
            prediction_dict = self.predictor.predict(transformed_features.as_dict())
            prediction = PredictionResult(**prediction_dict)
        except Exception as e:
            return {
                "status": "error",
                "stage": "prediction",
                "message": str(e)
            }

        explanation = self.explainer.build_explanation(prediction.as_dict())

        return {
            "status": "success",
            "patient": patient.file_name,
            "validation": validation_result,
            "base_features": base_features.as_dict(),
            "transformed_features": transformed_features.as_dict(),
            "prediction": prediction.as_dict(),
            "explanation": explanation
        }