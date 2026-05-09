from __future__ import annotations
from typing import Callable, Dict
import numpy as np


EPSILON = 1e-8


def _to_numpy(signal) -> np.ndarray:
    arr = np.asarray(signal, dtype=float).flatten()
    arr = arr[~np.isnan(arr)]

    if arr.size == 0:
        raise ValueError("Signal is empty after removing NaN values.")

    return arr


def median(signal) -> float:
    arr = _to_numpy(signal)
    return float(np.median(arr))


def q3(signal) -> float:
    arr = _to_numpy(signal)
    return float(np.percentile(arr, 75))


def mad(signal) -> float:

    arr = _to_numpy(signal)
    med = np.median(arr)
    return float(np.median(np.abs(arr - med)))


def iqr(signal) -> float:

    arr = _to_numpy(signal)
    q1 = np.percentile(arr, 25)
    q3_value = np.percentile(arr, 75)
    return float(q3_value - q1)


def value_range(signal) -> float:

    arr = _to_numpy(signal)
    return float(np.max(arr) - np.min(arr))


def lag_of_max(signal) -> int:

    arr = _to_numpy(signal)
    return int(np.argmax(arr))


def lag_of_min(signal) -> int:

    arr = _to_numpy(signal)
    return int(np.argmin(arr))


def zero_crossings(signal) -> int:

    arr = _to_numpy(signal)

    if arr.size < 2:
        return 0

    signs = np.sign(arr)

    for i in range(1, len(signs)):
        if signs[i] == 0:
            signs[i] = signs[i - 1]

    for i in range(len(signs) - 2, -1, -1):
        if signs[i] == 0:
            signs[i] = signs[i + 1]

    crossings = np.sum(signs[:-1] * signs[1:] < 0)
    return int(crossings)


def peak_count(signal) -> int:

    arr = _to_numpy(signal)

    if arr.size < 3:
        return 0

    peaks = 0
    for i in range(1, len(arr) - 1):
        if arr[i] > arr[i - 1] and arr[i] > arr[i + 1]:
            peaks += 1

    return peaks


def trough_count(signal) -> int:

    arr = _to_numpy(signal)

    if arr.size < 3:
        return 0

    troughs = 0
    for i in range(1, len(arr) - 1):
        if arr[i] < arr[i - 1] and arr[i] < arr[i + 1]:
            troughs += 1

    return troughs


def positive_fraction(signal) -> float:

    arr = _to_numpy(signal)
    return float(np.sum(arr > 0) / len(arr))


def pos_neg_auc_ratio(signal) -> float:

    arr = _to_numpy(signal)

    positive_area = float(np.sum(arr[arr > 0]))
    negative_area = float(abs(np.sum(arr[arr < 0])))

    return float(positive_area / (negative_area + EPSILON))


STAT_FUNCTIONS: Dict[str, Callable] = {
    "median": median,
    "q3": q3,
    "mad": mad,
    "iqr": iqr,
    "range": value_range,
    "lag_of_max": lag_of_max,
    "lag_of_min": lag_of_min,
    "zero_crossings": zero_crossings,
    "peak_count": peak_count,
    "trough_count": trough_count,
    "positive_fraction": positive_fraction,
    "pos_neg_auc_ratio": pos_neg_auc_ratio,
}


def compute_statistic(signal, stat_name: str):

    if stat_name not in STAT_FUNCTIONS:
        available = ", ".join(STAT_FUNCTIONS.keys())
        raise ValueError(
            f"Unsupported statistic '{stat_name}'. Available statistics: {available}"
        )

    return STAT_FUNCTIONS[stat_name](signal)