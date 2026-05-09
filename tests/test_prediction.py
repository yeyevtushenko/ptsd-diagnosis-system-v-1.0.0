import json

from backend.services.prediction_service import PredictionService


def load_test_features():
    with open("models/model_coefficients.json", "r", encoding="utf-8") as file:
        model_data = json.load(file)

    coefficients = model_data["coefficients"]

    return {
        feature: 0.0
        for feature in coefficients.keys()
    }


def test_prediction_service_returns_expected_keys():
    service = PredictionService("models/model_coefficients.json")
    features = load_test_features()

    result = service.predict(features)

    expected_keys = {
        "z",
        "probability",
        "probability_class_1",
        "probability_class_0",
        "predicted_probability",
        "predicted_class",
        "threshold",
        "intercept",
        "feature_contributions",
    }

    assert expected_keys.issubset(result.keys())


def test_prediction_probabilities_sum_to_one():
    service = PredictionService("models/model_coefficients.json")
    features = load_test_features()

    result = service.predict(features)

    total_probability = (
            result["probability_class_0"] + result["probability_class_1"]
    )

    assert abs(total_probability - 1.0) < 1e-6


def test_predicted_probability_matches_predicted_class():
    service = PredictionService("models/model_coefficients.json")
    features = load_test_features()

    result = service.predict(features)

    if result["predicted_class"] == 1:
        assert result["predicted_probability"] == result["probability_class_1"]
    else:
        assert result["predicted_probability"] == result["probability_class_0"]
