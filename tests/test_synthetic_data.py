from __future__ import annotations

import csv
import hashlib
import json
import math
import unittest
from pathlib import Path

from darius_demo.schema import CLASS_LABELS, FEATURE_NAMES, FEATURE_ORDER_HASH
from darius_demo.synthetic import CITY_RULES, SPLIT_ROWS, generate_all


def file_hashes(root: Path) -> dict[str, str]:
    return {
        path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


class SyntheticDataTests(unittest.TestCase):
    def test_regeneration_is_byte_deterministic(self) -> None:
        root = Path(__file__).resolve().parents[1]
        first = root / ".determinism-a"
        second = root / ".determinism-b"
        first_root = first / "synthetic-data" / "generated"
        second_root = second / "synthetic-data" / "generated"
        generate_all(first_root)
        generate_all(second_root)
        self.assertEqual(file_hashes(first), file_hashes(second))

    def test_contract_finite_values_and_class_support(self) -> None:
        root = Path(__file__).resolve().parents[1] / "synthetic-data" / "generated"
        for city in CITY_RULES:
            observed_classes: set[str] = set()
            for split, expected_count in SPLIT_ROWS.items():
                with (root / city / f"{split}.csv").open(encoding="utf-8", newline="") as handle:
                    reader = csv.DictReader(handle)
                    feature_columns = [name for name in reader.fieldnames or [] if name in FEATURE_NAMES]
                    self.assertEqual(feature_columns, FEATURE_NAMES)
                    rows = list(reader)
                self.assertEqual(len(rows), expected_count)
                for row in rows:
                    self.assertTrue(all(math.isfinite(float(row[name])) for name in FEATURE_NAMES))
                    observed_classes.add(row["load_level"])
                self.assertEqual({row["load_level"] for row in rows}, set(CLASS_LABELS))
            self.assertEqual(observed_classes, set(CLASS_LABELS))
            metadata = json.loads((root / city / "metadata.json").read_text(encoding="utf-8"))
            self.assertTrue(metadata["synthetic_only"])
            self.assertEqual(metadata["feature_order_hash"], FEATURE_ORDER_HASH)


if __name__ == "__main__":
    unittest.main()
