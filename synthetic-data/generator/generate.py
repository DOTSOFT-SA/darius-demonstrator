from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from darius_demo.synthetic import generate_all

if __name__ == "__main__":
    generate_all(ROOT / "synthetic-data" / "generated")
    print("Generated deterministic synthetic datasets and manifest.")
