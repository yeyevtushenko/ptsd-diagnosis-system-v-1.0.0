import numpy as np
import pytest

from utils.statistics import STAT_FUNCTIONS, compute_statistic


def test_stat_functions_are_registered():
    expected_statistics = {
        "median",
        "q3",
        "mad",
        "iqr",
        "range",
        "lag_of_max",
        "lag_of_min",
        "zero_crossings",
        "peak_count",
        "trough_count",
        "positive_fraction",
        "pos_neg_auc_ratio",
    }

    assert expected_statistics.issubset(STAT_FUNCTIONS.keys())


def test_compute_statistic_returns_numeric_values():
    signal = np.array([-2, -1, 0, 1, 3, 2, -1], dtype=float)

    for stat_name in STAT_FUNCTIONS.keys():
        value = compute_statistic(signal, stat_name)

        assert isinstance(value, (int, float, np.integer, np.floating))


def test_compute_statistic_rejects_unknown_statistic():
    signal = np.array([1, 2, 3], dtype=float)

    with pytest.raises(ValueError):
        compute_statistic(signal, "unknown_statistic")


def test_compute_statistic_rejects_empty_signal():
    signal = np.array([np.nan, np.nan])

    with pytest.raises(ValueError):
        compute_statistic(signal, "median")