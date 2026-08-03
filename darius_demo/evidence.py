from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


class EvidenceLog:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.events: list[dict[str, object]] = []

    def append(self, event_type: str, details: dict[str, object]) -> dict[str, object]:
        previous_hash = str(self.events[-1]["event_hash"]) if self.events else "0" * 64
        event: dict[str, object] = {
            "sequence": len(self.events) + 1,
            "timestamp": datetime(2035, 1, 1, tzinfo=timezone.utc).isoformat(),
            "event_type": event_type,
            "details": details,
            "previous_hash": previous_hash,
        }
        canonical = json.dumps(event, sort_keys=True, separators=(",", ":"))
        event["event_hash"] = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
        self.events.append(event)
        self.path.write_text("".join(json.dumps(item, sort_keys=True) + "\n" for item in self.events), encoding="utf-8")
        return event


def verify_evidence(path: Path) -> bool:
    previous_hash = "0" * 64
    for expected_sequence, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        event = json.loads(line)
        claimed_hash = event.pop("event_hash")
        if event["sequence"] != expected_sequence or event["previous_hash"] != previous_hash:
            return False
        canonical = json.dumps(event, sort_keys=True, separators=(",", ":"))
        if hashlib.sha256(canonical.encode("utf-8")).hexdigest() != claimed_hash:
            return False
        previous_hash = claimed_hash
    return True
