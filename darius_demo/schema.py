from __future__ import annotations

import hashlib
import json

SCHEMA_VERSION = "phase7_load_core_plus_lags_v1"
FEATURE_NAMES = [
    "occupancy_rate",
    "active_sensors",
    "avg_time_since_change",
    "avg_prev_state_duration",
    "dow",
    "time_bucket",
    "dow_time_bucket",
    "is_weekend",
    "is_holiday",
    "hour_sin",
    "hour_cos",
    "dow_sin",
    "dow_cos",
    "roll_occ_rate_4",
    "roll_turnover_4",
    "roll_occ_rate_12",
    "roll_turnover_12",
    "roll_occ_rate_24",
    "roll_turnover_24",
    "roll_departure_rate_4",
    "occupancy_lag_1",
    "occupancy_lag_4",
    "occupancy_lag_12",
    "occupancy_lag_96",
]
CLASS_LABELS = ["low", "medium", "high"]
CLASS_MAPPING = {"low": 0, "medium": 1, "high": 2}
TARGET_COLUMN = "load_level_code"


def feature_order_hash() -> str:
    payload = json.dumps(FEATURE_NAMES, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


FEATURE_ORDER_HASH = feature_order_hash()
