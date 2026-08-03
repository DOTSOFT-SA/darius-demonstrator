from __future__ import annotations

import csv
import hashlib
import json
import math
import random
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path

from .schema import CLASS_LABELS, CLASS_MAPPING, FEATURE_NAMES, FEATURE_ORDER_HASH, SCHEMA_VERSION

CITY_RULES = {
    "synthetic_city_alpha": {"seed": 104729, "capacity": 160, "base": 0.42, "am": 0.34, "pm": 0.22, "phase": 0.0},
    "synthetic_city_beta": {"seed": 130363, "capacity": 240, "base": 0.55, "am": 0.18, "pm": 0.35, "phase": 1.2},
    "synthetic_city_gamma": {"seed": 155921, "capacity": 110, "base": 0.40, "am": 0.40, "pm": 0.40, "phase": -0.8},
}
SPLIT_ROWS = {"train": 672, "val": 192, "test": 192}
START = datetime(2035, 1, 1, tzinfo=timezone.utc)


def _clip(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def _mean(values: list[float]) -> float:
    return sum(values) / len(values)


def _window(values: list[float], end: int, width: int) -> list[float]:
    start = max(0, end - width + 1)
    result = values[start : end + 1]
    return result or [values[0]]


def _level(future_occupancy: float) -> tuple[int, str]:
    if future_occupancy >= 0.80:
        return CLASS_MAPPING["high"], "high"
    if future_occupancy >= 0.60:
        return CLASS_MAPPING["medium"], "medium"
    return CLASS_MAPPING["low"], "low"


def generate_city_rows(city: str) -> list[dict[str, object]]:
    rule = CITY_RULES[city]
    rng = random.Random(rule["seed"])
    total = sum(SPLIT_ROWS.values())
    occupancy: list[float] = []
    for index in range(total + 4):
        timestamp = START + timedelta(minutes=15 * index)
        hour = timestamp.hour + timestamp.minute / 60.0
        weekday_factor = 0.88 if timestamp.weekday() >= 5 else 1.0
        morning = math.exp(-((hour - (8.5 + rule["phase"])) / 2.6) ** 2)
        evening = math.exp(-((hour - (17.0 + rule["phase"] / 2)) / 3.0) ** 2)
        daily_wave = 0.08 * math.sin(2 * math.pi * hour / 24 + rule["phase"])
        value = (rule["base"] + rule["am"] * morning + rule["pm"] * evening + daily_wave) * weekday_factor
        occupancy.append(_clip(value + rng.uniform(-0.035, 0.035), 0.05, 0.96))

    rows: list[dict[str, object]] = []
    turnover: list[float] = [0.0]
    departures: list[float] = [0.0]
    for index in range(total):
        timestamp = START + timedelta(minutes=15 * index)
        occ = occupancy[index]
        change = abs(occ - occupancy[max(0, index - 1)])
        turnover.append(change * rule["capacity"])
        departures.append(max(0.0, occupancy[max(0, index - 1)] - occ) * rule["capacity"])
        dow = timestamp.weekday()
        bucket = timestamp.hour * 4 + timestamp.minute // 15
        hour = timestamp.hour + timestamp.minute / 60.0
        future_code, future_label = _level(occupancy[index + 4])
        feature_values = {
            "occupancy_rate": occ,
            "active_sensors": float(round(rule["capacity"] * (0.965 + rng.uniform(-0.01, 0.01)))),
            "avg_time_since_change": 90.0 + (1.0 - change) * 720.0 + rng.uniform(0.0, 45.0),
            "avg_prev_state_duration": 180.0 + (1.0 - change) * 1500.0 + rng.uniform(0.0, 90.0),
            "dow": float(dow),
            "time_bucket": float(bucket),
            "dow_time_bucket": float(dow * 96 + bucket),
            "is_weekend": float(dow >= 5),
            "is_holiday": 0.0,
            "hour_sin": math.sin(2 * math.pi * hour / 24),
            "hour_cos": math.cos(2 * math.pi * hour / 24),
            "dow_sin": math.sin(2 * math.pi * dow / 7),
            "dow_cos": math.cos(2 * math.pi * dow / 7),
            "roll_occ_rate_4": _mean(_window(occupancy, index, 4)),
            "roll_turnover_4": _mean(_window(turnover, len(turnover) - 1, 4)),
            "roll_occ_rate_12": _mean(_window(occupancy, index, 12)),
            "roll_turnover_12": _mean(_window(turnover, len(turnover) - 1, 12)),
            "roll_occ_rate_24": _mean(_window(occupancy, index, 24)),
            "roll_turnover_24": _mean(_window(turnover, len(turnover) - 1, 24)),
            "roll_departure_rate_4": _mean(_window(departures, len(departures) - 1, 4)),
            "occupancy_lag_1": occupancy[max(0, index - 1)],
            "occupancy_lag_4": occupancy[max(0, index - 4)],
            "occupancy_lag_12": occupancy[max(0, index - 12)],
            "occupancy_lag_96": occupancy[max(0, index - 96)],
        }
        row: dict[str, object] = {"timestamp": timestamp.isoformat().replace("+00:00", "Z")}
        row.update({name: round(float(feature_values[name]), 8) for name in FEATURE_NAMES})
        row["load_level_code"] = future_code
        row["load_level"] = future_label
        rows.append(row)
    return rows


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(65536), b""):
            digest.update(block)
    return digest.hexdigest()


def generate_all(output_root: Path) -> dict[str, object]:
    output_root.mkdir(parents=True, exist_ok=True)
    manifest_dir = output_root.parent / "manifests"
    manifest_dir.mkdir(parents=True, exist_ok=True)
    file_records: list[dict[str, object]] = []
    for city in CITY_RULES:
        rows = generate_city_rows(city)
        city_dir = output_root / city
        city_dir.mkdir(parents=True, exist_ok=True)
        offset = 0
        city_counts: Counter[str] = Counter()
        for split, count in SPLIT_ROWS.items():
            split_rows = rows[offset : offset + count]
            offset += count
            path = city_dir / f"{split}.csv"
            with path.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=["timestamp", *FEATURE_NAMES, "load_level_code", "load_level"], lineterminator="\n")
                writer.writeheader()
                writer.writerows(split_rows)
            split_counts = Counter(str(row["load_level"]) for row in split_rows)
            if any(split_counts[label] == 0 for label in CLASS_LABELS):
                raise RuntimeError(f"Synthetic rules did not produce all classes for {city}/{split}.")
            city_counts.update(split_counts)
            file_records.append({
                "path": path.relative_to(output_root.parent.parent).as_posix(),
                "sha256": _sha256(path),
                "rows": count,
                "class_counts": {label: split_counts[label] for label in CLASS_LABELS},
            })
        if any(city_counts[label] == 0 for label in CLASS_LABELS):
            raise RuntimeError(f"Synthetic rules did not produce all classes for {city}.")
        metadata = {
            "city_id": city,
            "fictional": True,
            "synthetic_only": True,
            "seed": CITY_RULES[city]["seed"],
            "schema_version": SCHEMA_VERSION,
            "feature_names": FEATURE_NAMES,
            "feature_order_hash": FEATURE_ORDER_HASH,
            "class_mapping": CLASS_MAPPING,
            "row_counts": SPLIT_ROWS,
            "class_counts": {label: city_counts[label] for label in CLASS_LABELS},
        }
        metadata_path = city_dir / "metadata.json"
        metadata_path.write_text(json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        file_records.append({"path": metadata_path.relative_to(output_root.parent.parent).as_posix(), "sha256": _sha256(metadata_path)})

    manifest = {
        "manifest_version": 1,
        "provenance": "Generated independently from documented mathematical rules; no municipal rows or artifacts are inputs.",
        "schema_version": SCHEMA_VERSION,
        "feature_order_hash": FEATURE_ORDER_HASH,
        "cities": {city: {"seed": rule["seed"], "row_counts": SPLIT_ROWS} for city, rule in CITY_RULES.items()},
        "files": sorted(file_records, key=lambda item: str(item["path"])),
    }
    manifest_path = manifest_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return manifest
