from __future__ import annotations

from pathlib import Path

import numpy as np

from darius_demo.model import standardize, train_local
from darius_demo.schema import FEATURE_NAMES
from darius_demo.synthetic import SPLIT_ROWS, generate_city_rows


ROOT = Path(__file__).resolve().parents[1]


def load_city(
    city: str,
    split: str,
    means: list[float],
    scales: list[float],
) -> tuple[list[list[float]], list[int]]:
    rows = generate_city_rows(city)
    split_order = tuple(SPLIT_ROWS)
    if split not in split_order:
        raise ValueError(f"Unknown data split: {split}")
    start = sum(SPLIT_ROWS[name] for name in split_order[: split_order.index(split)])
    selected = rows[start : start + SPLIT_ROWS[split]]
    values = [
        [float(row[name]) for name in FEATURE_NAMES]
        for row in selected
    ]
    labels = [int(row["load_level_code"]) for row in selected]
    return standardize(values, means, scales), labels


def train_parameters(
    parameters: list[np.ndarray],
    rows: list[list[float]],
    labels: list[int],
) -> list[np.ndarray]:
    weights = parameters[0].astype(float).tolist()
    bias = parameters[1].astype(float).tolist()
    weights, bias = train_local(weights, bias, rows, labels)
    return [
        np.asarray(weights, dtype=np.float64),
        np.asarray(bias, dtype=np.float64),
    ]
