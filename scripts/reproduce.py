from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from darius_demo.evidence import EvidenceLog
from darius_demo.model import aggregate, accuracy, export_onnx, fit_scaler, read_split, save_model, standardize, train_local, zero_parameters
from darius_demo.synthetic import CITY_RULES, generate_all


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def reproduce(rounds: int = 3) -> dict[str, object]:
    data_root = ROOT / "synthetic-data" / "generated"
    manifest = generate_all(data_root)
    evidence = EvidenceLog(ROOT / "evidence" / "events.jsonl")
    evidence.append("synthetic_data_generated", {"manifest_sha256": sha256(ROOT / "synthetic-data" / "manifests" / "manifest.json")})
    raw: dict[str, dict[str, tuple[list[list[float]], list[int]]]] = {}
    for city in CITY_RULES:
        raw[city] = {split: read_split(data_root / city / f"{split}.csv") for split in ("train", "val", "test")}
    means, scales = fit_scaler(raw[city]["train"][0] for city in CITY_RULES)
    prepared = {
        city: {
            split: (standardize(values, means, scales), labels)
            for split, (values, labels) in splits.items()
        }
        for city, splits in raw.items()
    }
    weights, bias = zero_parameters()
    history: list[dict[str, object]] = []
    for round_number in range(1, rounds + 1):
        updates = []
        local_metrics: dict[str, float] = {}
        for city in CITY_RULES:
            train_x, train_y = prepared[city]["train"]
            local_w, local_b = train_local(weights, bias, train_x, train_y)
            updates.append((local_w, local_b, len(train_y)))
            val_x, val_y = prepared[city]["val"]
            local_metrics[city] = round(accuracy(val_x, val_y, local_w, local_b), 6)
            evidence.append("local_update_accepted", {"round": round_number, "city_id": city, "examples": len(train_y)})
        weights, bias = aggregate(updates)
        round_result = {"round": round_number, "validation_accuracy": local_metrics}
        history.append(round_result)
        evidence.append("round_aggregated", round_result)
    test_metrics = {}
    for city in CITY_RULES:
        test_x, test_y = prepared[city]["test"]
        test_metrics[city] = round(accuracy(test_x, test_y, weights, bias), 6)
    json_path = ROOT / "browser-edge-client" / "public" / "models" / "synthetic_softmax.json"
    onnx_path = ROOT / "browser-edge-client" / "public" / "models" / "synthetic_softmax.onnx"
    example = raw["synthetic_city_alpha"]["test"][0][0]
    summary = {"rounds": rounds, "city_test_accuracy": test_metrics, "history": history}
    save_model(json_path, weights=weights, bias=bias, means=means, scales=scales, example=example, training=summary)
    export_onnx(json_path, onnx_path)
    evidence.append("browser_artifacts_exported", {"json_sha256": sha256(json_path), "onnx_sha256": sha256(onnx_path), "synthetic_only": True})
    summary["artifacts"] = {"json": sha256(json_path), "onnx": sha256(onnx_path)}
    summary["dataset_file_count"] = len(manifest["files"])
    summary_path = ROOT / "evidence" / "reproduction_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Reproduce the synthetic DARIUS demonstrator artifacts.")
    parser.add_argument("--rounds", type=int, default=3)
    args = parser.parse_args()
    print(json.dumps(reproduce(args.rounds), indent=2, sort_keys=True))
