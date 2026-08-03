from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from darius_demo.evidence import verify_evidence
from scripts.reproduce import reproduce


def main() -> None:
    parser = argparse.ArgumentParser(description="Run and verify the synthetic DARIUS orchestration/evidence flow.")
    parser.add_argument("--rounds", type=int, default=3)
    args = parser.parse_args()
    summary = reproduce(args.rounds)
    evidence_path = ROOT / "evidence" / "events.jsonl"
    if not verify_evidence(evidence_path):
        raise SystemExit("Evidence hash-chain verification failed.")
    print(json.dumps({"status": "complete", "evidence_verified": True, "summary": summary}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
