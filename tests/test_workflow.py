from __future__ import annotations

import json
import unittest
from pathlib import Path

import numpy as np
import onnxruntime as ort

from darius_demo.evidence import verify_evidence
from darius_demo.model import probabilities, standardize
from scripts.reproduce import reproduce


ROOT = Path(__file__).resolve().parents[1]


class WorkflowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        reproduce(rounds=2)

    def test_evidence_chain(self) -> None:
        self.assertTrue(verify_evidence(ROOT / "evidence" / "events.jsonl"))

    def test_json_onnx_parity(self) -> None:
        model_path = ROOT / "browser-edge-client" / "public" / "models" / "synthetic_softmax.json"
        model = json.loads(model_path.read_text(encoding="utf-8"))
        scaled = standardize([model["example_input"]], model["scaler_mean"], model["scaler_scale"])[0]
        expected = probabilities(scaled, model["weights"], model["bias"])
        session = ort.InferenceSession(str(model_path.with_suffix(".onnx")), providers=["CPUExecutionProvider"])
        actual = session.run(None, {"features": np.asarray([scaled], dtype=np.float32)})[0][0]
        np.testing.assert_allclose(actual, expected, rtol=1e-5, atol=1e-6)

    def test_model_is_explicitly_synthetic_only(self) -> None:
        model = json.loads((ROOT / "browser-edge-client" / "public" / "models" / "synthetic_softmax.json").read_text(encoding="utf-8"))
        self.assertTrue(model["demonstration_only"])
        self.assertTrue(model["training_data_provenance"].startswith("synthetic-only"))


if __name__ == "__main__":
    unittest.main()
