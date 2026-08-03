# Third-party notices

No dependency source code, runtime binaries, logos, or other third-party assets are vendored in this candidate. Dependencies are installed through Python's and Node's package managers.

The directly declared dependencies and the licence metadata inspected from the locally installed packages used for validation are:

| Dependency | Declared range/version | Licence |
|---|---:|---|
| Flower (`flwr`) | `>=1.32,<1.33` (inspected 1.32.1) | Apache-2.0 |
| NumPy | `>=1.26,<3` (inspected 2.4.6) | BSD-3-Clause and bundled component licences |
| ONNX | `>=1.16,<2` (inspected 1.21.0) | Apache-2.0 |
| ONNX Runtime / `onnxruntime-web` | `>=1.18,<2` / 1.26.0 | MIT |
| Vite | 7.3.3 | MIT |

Transitive dependencies have their own terms. Before publication, generate and review a locked dependency inventory in the intended clean build environment. This file is a notice, not legal advice and not a substitute for that final review.
