# Architecture

The release candidate keeps one narrow path from generation to browser result:

```text
darius_demo.synthetic
  └─ deterministic CSV splits + manifest
       ├─ offline orchestrator ── local softmax updates ── weighted aggregation
       │      └─ hash-chained evidence + JSON/ONNX browser artifacts
       └─ ClientApps on SuperNodes ── SuperLink + ServerApp ── network-run summary

browser-edge-client
  ├─ JSON weights → JavaScript scaler + softmax
  └─ ONNX graph   → ONNX Runtime Web WASM
```

`darius_demo` is shared to prevent the offline verifier and Flower App from
drifting on schema or training logic. The SuperLink/SuperNode launcher is the
networked demonstration. The orchestrator is the fast deterministic
reproduction/evidence path. Neither is a production control plane.

Only parameters, bias values, example counts, and metrics cross the Flower interface. CSV records remain local to each fictional client. This architectural fact is not a privacy guarantee: the package implements neither secure aggregation nor differential privacy.
