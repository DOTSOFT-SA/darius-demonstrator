from __future__ import annotations

import csv
import json
import math
from pathlib import Path
from typing import Iterable

from .schema import CLASS_LABELS, CLASS_MAPPING, FEATURE_NAMES, FEATURE_ORDER_HASH, SCHEMA_VERSION


def read_split(path: Path) -> tuple[list[list[float]], list[int]]:
    features: list[list[float]] = []
    labels: list[int] = []
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        observed = [name for name in (reader.fieldnames or []) if name in FEATURE_NAMES]
        if observed != FEATURE_NAMES:
            raise ValueError(f"Feature order mismatch in {path}")
        for row in reader:
            values = [float(row[name]) for name in FEATURE_NAMES]
            if not all(math.isfinite(value) for value in values):
                raise ValueError(f"Non-finite feature in {path}")
            features.append(values)
            labels.append(int(row["load_level_code"]))
    return features, labels


def fit_scaler(matrices: Iterable[list[list[float]]]) -> tuple[list[float], list[float]]:
    rows = [row for matrix in matrices for row in matrix]
    means = [sum(row[j] for row in rows) / len(rows) for j in range(len(FEATURE_NAMES))]
    scales = []
    for j, mean in enumerate(means):
        variance = sum((row[j] - mean) ** 2 for row in rows) / len(rows)
        scale = math.sqrt(variance)
        scales.append(scale if scale > 0.0 else 1.0)
    return means, scales


def standardize(rows: list[list[float]], means: list[float], scales: list[float]) -> list[list[float]]:
    return [[(value - means[j]) / scales[j] for j, value in enumerate(row)] for row in rows]


def zero_parameters() -> tuple[list[list[float]], list[float]]:
    return [[0.0 for _ in CLASS_LABELS] for _ in FEATURE_NAMES], [0.0 for _ in CLASS_LABELS]


def probabilities(row: list[float], weights: list[list[float]], bias: list[float]) -> list[float]:
    logits = [bias[k] + sum(row[j] * weights[j][k] for j in range(len(row))) for k in range(len(CLASS_LABELS))]
    peak = max(logits)
    exp_values = [math.exp(value - peak) for value in logits]
    total = sum(exp_values)
    return [value / total for value in exp_values]


def train_local(
    initial_weights: list[list[float]],
    initial_bias: list[float],
    rows: list[list[float]],
    labels: list[int],
    *,
    epochs: int = 4,
    learning_rate: float = 0.08,
) -> tuple[list[list[float]], list[float]]:
    weights = [row[:] for row in initial_weights]
    bias = initial_bias[:]
    count = len(rows)
    for _ in range(epochs):
        grad_w = [[0.0 for _ in CLASS_LABELS] for _ in FEATURE_NAMES]
        grad_b = [0.0 for _ in CLASS_LABELS]
        for row, label in zip(rows, labels):
            probs = probabilities(row, weights, bias)
            for k in range(len(CLASS_LABELS)):
                error = probs[k] - float(k == label)
                grad_b[k] += error
                for j, value in enumerate(row):
                    grad_w[j][k] += value * error
        for j in range(len(FEATURE_NAMES)):
            for k in range(len(CLASS_LABELS)):
                weights[j][k] -= learning_rate * grad_w[j][k] / count
        for k in range(len(CLASS_LABELS)):
            bias[k] -= learning_rate * grad_b[k] / count
    return weights, bias


def aggregate(updates: list[tuple[list[list[float]], list[float], int]]) -> tuple[list[list[float]], list[float]]:
    total = sum(count for _, _, count in updates)
    weights, bias = zero_parameters()
    for local_w, local_b, count in updates:
        fraction = count / total
        for j in range(len(FEATURE_NAMES)):
            for k in range(len(CLASS_LABELS)):
                weights[j][k] += local_w[j][k] * fraction
        for k in range(len(CLASS_LABELS)):
            bias[k] += local_b[k] * fraction
    return weights, bias


def accuracy(rows: list[list[float]], labels: list[int], weights: list[list[float]], bias: list[float]) -> float:
    correct = sum(max(range(len(CLASS_LABELS)), key=lambda k: probabilities(row, weights, bias)[k]) == label for row, label in zip(rows, labels))
    return correct / len(rows)


def save_model(path: Path, *, weights: list[list[float]], bias: list[float], means: list[float], scales: list[float], example: list[float], training: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "artifact_version": 1,
        "model_family": "softmax_classifier",
        "parameter_format": "features_by_classes_weights_bias_v1",
        "demonstration_only": True,
        "training_data_provenance": "synthetic-only: synthetic_city_alpha, synthetic_city_beta, synthetic_city_gamma",
        "schema_version": SCHEMA_VERSION,
        "feature_names": FEATURE_NAMES,
        "feature_order_hash": FEATURE_ORDER_HASH,
        "classes": CLASS_LABELS,
        "class_mapping": CLASS_MAPPING,
        "scaler_mean": means,
        "scaler_scale": scales,
        "weights": weights,
        "bias": bias,
        "example_input": example,
        "training_summary": training,
    }
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def export_onnx(json_path: Path, onnx_path: Path) -> None:
    try:
        import numpy as np
        import onnx
        from onnx import TensorProto, helper, numpy_helper
    except ImportError as exc:
        raise RuntimeError("ONNX export requires the packages listed in requirements.txt") from exc
    model = json.loads(json_path.read_text(encoding="utf-8"))
    weights = np.asarray(model["weights"], dtype=np.float32)
    bias = np.asarray(model["bias"], dtype=np.float32)
    graph = helper.make_graph(
        [
            helper.make_node("Gemm", ["features", "weights", "bias"], ["logits"]),
            helper.make_node("Softmax", ["logits"], ["probabilities"], axis=1),
        ],
        "darius_synthetic_softmax",
        [helper.make_tensor_value_info("features", TensorProto.FLOAT, [None, len(FEATURE_NAMES)])],
        [helper.make_tensor_value_info("probabilities", TensorProto.FLOAT, [None, len(CLASS_LABELS)])],
        [numpy_helper.from_array(weights, "weights"), numpy_helper.from_array(bias, "bias")],
    )
    graph_model = helper.make_model(graph, producer_name="darius-synthetic-demo", opset_imports=[helper.make_opsetid("", 13)])
    graph_model.ir_version = 8
    onnx.helper.set_model_props(graph_model, {
        "demonstration_only": "true",
        "training_data_provenance": "synthetic-only",
        "feature_order_hash": FEATURE_ORDER_HASH,
    })
    onnx.checker.check_model(graph_model)
    onnx_path.parent.mkdir(parents=True, exist_ok=True)
    onnx.save_model(graph_model, onnx_path)
