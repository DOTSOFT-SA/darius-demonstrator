<p align="center">
  <img
    src="docs/assets/darius-logo.png"
    alt="DARIUS, dAIEDGE, European Union funding, and DOTSOFT"
    width="900"
  >
</p>

# DARIUS Demonstrator

**Publication status:** DOTSOFT S.A. has published the DARIUS synthetic-data demonstrator under the [MIT License](LICENSE). The canonical public repository is [DOTSOFT-SA/darius-demonstrator](https://github.com/DOTSOFT-SA/darius-demonstrator).

DARIUS demonstrates an inspectable and reproducible federated-learning workflow for fictional parking-load environments. It generates independent synthetic data, trains a three-client federated classifier, records orchestration evidence, exports JSON and ONNX models, and runs both model formats locally in a browser.

## Components and flow

```text
seeded mathematical rules
        │
        ├── synthetic_city_alpha CSVs ─┐
        ├── synthetic_city_beta CSVs  ├── local training ── weighted FedAvg
        └── synthetic_city_gamma CSVs ┘                         │
                                                                ├── hash-chained evidence
                                                                ├── JSON model ─┐
                                                                └── ONNX model ─┴── browser-local inference + bounded what-if
```

- `synthetic-data/`: reproducible train, validation, and test CSVs for three explicitly fictional cities.
- `darius_fl_app/`: current Flower `ServerApp` and `ClientApp` components using the Message API.
- `flower-federated-learning/`: a launcher for one SuperLink and three synthetic-city SuperNodes.
- `fl-orchestrator/`: the deterministic end-to-end runner and evidence-chain verifier.
- `browser-edge-client/`: Vite application comparing local JSON and ONNX inference.
- `darius_demo/`: small shared implementation of the canonical schema, generator, model, aggregation, export, and evidence logic.
- `tests/`: contract, determinism, provenance, evidence, and JSON/ONNX parity tests.

See [architecture](docs/architecture.md), [data contract](docs/data-contract.md), and [privacy design](docs/privacy-and-synthetic-data.md).

## Prerequisites

- Python 3.10–3.13 is the supported public target. Validation also succeeded with Python 3.14.5.
- Node.js 20 or later and npm.
- Five terminals only when inspecting the networked Flower processes manually.

No database, cloud service, container, credentials, or municipal data are required.

## Install

From the repository root:

```bash
python -m venv .venv
```

Activate the environment using your shell, then install the reproduction dependencies:

```bash
python -m pip install -r requirements.txt
```

For the networked Flower workflow also run:

```bash
python -m pip install -r flower-federated-learning/requirements.txt
```

Install the locked browser dependencies:

```bash
npm ci --prefix browser-edge-client
```

Dependencies are installed through the declared package files. Their applicable notices are documented in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

## Generate synthetic data

```bash
python synthetic-data/generator/generate.py
```

This rewrites only public generated artifacts under `synthetic-data/generated/` and `synthetic-data/manifests/`. Seeds, rules, row counts, and hashes are documented in [synthetic-data/README.md](synthetic-data/README.md). No real row is read or transformed.

## Reproduce the complete offline workflow

```bash
python fl-orchestrator/orchestrate_demo.py --rounds 3
```

Expected results:

- 12 CSV split files/metadata records plus a deterministic manifest;
- three accepted local updates and one aggregation event per round;
- `evidence/events.jsonl` with a valid SHA-256 hash chain;
- `evidence/reproduction_summary.json`;
- `browser-edge-client/public/models/synthetic_softmax.json`;
- `browser-edge-client/public/models/synthetic_softmax.onnx`;
- terminal JSON containing `"status": "complete"` and `"evidence_verified": true`.

The runner provides a deterministic, single-process reproduction path using the same local-training and weighted-aggregation logic as the networked workflow.

## Run the networked Flower workflow

Generate artifacts first. The simplest reproducible command starts one SuperLink,
three SuperNodes, and submits the Flower App with `flwr run`:

```bash
python flower-federated-learning/run_demo.py --rounds 3
```

Successful completion ends with:

```text
FLOWER DEMO COMPLETE
```

and a JSON result containing `accepted_clients: 3`, `failures: 0`,
`flower_runtime: "SuperLink/SuperNode"`, `round: 3`,
`weights_shape: [24, 3]`, and `bias_shape: [3]`.

A 20-round run needs a larger timeout:

```bash
python flower-federated-learning/run_demo.py --rounds 20 --workflow-timeout 1200
```

This is the recommended Flower 1.32 deployment architecture. It uses
`ServerApp`, `ClientApp`, `ArrayRecord`, `MetricRecord`, SuperLink,
SuperNode, and `flwr run`; it does not call the deprecated
`start_server()` or `start_client()` functions.

To inspect every current-standard process manually in PowerShell, first create
an isolated Flower CLI connection configuration:

```powershell
$env:FLWR_HOME = "$PWD\.flower-runtime"
New-Item -ItemType Directory -Force $env:FLWR_HOME | Out-Null
@'
[superlink]
default = "darius-local"

[superlink.darius-local]
address = "127.0.0.1:9093"
insecure = true
'@ | Set-Content "$env:FLWR_HOME\config.toml"
$env:DARIUS_DEMO_ROOT = "$PWD"
```

Keep the environment variables above in each terminal. Start the SuperLink:

```powershell
flower-superlink --insecure --disable-runtime-dependency-installation
```

Start one SuperNode in each of three additional terminals:

```powershell
flower-supernode --insecure --superlink 127.0.0.1:9092 --clientappio-api-address 127.0.0.1:9094 --node-config 'city="synthetic_city_alpha"'
flower-supernode --insecure --superlink 127.0.0.1:9092 --clientappio-api-address 127.0.0.1:9095 --node-config 'city="synthetic_city_beta"'
flower-supernode --insecure --superlink 127.0.0.1:9092 --clientappio-api-address 127.0.0.1:9096 --node-config 'city="synthetic_city_gamma"'
```

Finally submit the app from a fifth terminal:

```powershell
flwr run . darius-local --stream --run-config "num-server-rounds=3"
```

Flower then runs three weighted FedAvg rounds and writes
`evidence/flower_network_result.json`. SuperNodes exchange model arrays,
example counts, and metrics; they do not send CSV rows. The Browser Edge Client
is a separate inference UI and is not a training SuperNode.

The documented launcher uses local loopback connections for reproducible multi-process execution. For communication across separate machines, configure TLS and authenticated Flower connections according to the deployment environment.

## Launch the Browser Edge Client

```bash
npm run dev --prefix browser-edge-client
```

Open the loopback URL printed by Vite. The initial comparison now runs automatically. A working demo shows populated JSON and ONNX result panels and:

```text
Local format parity: PASS
```

Move the bounded ±15-percentage-point slider and select **Run both local formats** again. The probabilities should change, while both panels should remain equal within the reported tolerance. The page:

1. loads only synthetic-only model artifacts bundled with the demonstrator;
2. applies the same scaler locally;
3. runs pure JavaScript JSON inference;
4. runs ONNX Runtime Web inference in-browser;
5. reports class/probability parity;
6. makes no network request after loading application assets.

The what-if applies a bounded sensitivity analysis to selected occupancy-history fields and displays the corresponding model response.

## Test and build

```bash
python -m unittest discover -s tests -v
npm test --prefix browser-edge-client
npm run build --prefix browser-edge-client
```

For a clean-room reproduction sequence, follow [docs/reproduction-guide.md](docs/reproduction-guide.md).

## Troubleshooting

- `ModuleNotFoundError: onnx`: activate the Python environment and install `requirements.txt`.
- Flower waits for nodes: confirm all three SuperNodes are connected to the SuperLink Fleet API at port 9092.
- `Required local ports are already in use`: stop old Flower processes with `Ctrl+C` or pass an unused range, for example `--base-port 19091`.
- `flwr run` cannot find `darius-local`: use the one-command launcher, or recreate the documented `$env:FLWR_HOME\config.toml`.
- The `--insecure` option is used for local loopback execution. Configure TLS and authenticated connections before running Flower across separate machines.
- Browser model request returns 404: launch Vite from the package root using the documented `--prefix` command; do not open `index.html` directly.
- Page stays at `Loading…` or reports an ONNX runtime error: stop the Vite process, run `npm ci --prefix browser-edge-client`, restart it, and force-refresh the page with `Ctrl+F5`.
- ONNX WASM fails under a restrictive browser policy: use a current Chromium or Firefox build and confirm Vite is serving the app over loopback HTTP.
- Reproduction hashes changed: confirm source files and dependency versions are unchanged, then inspect `git diff`; CSV and JSON hashes should be byte-stable.

## Privacy and synthetic-only statement

Every included CSV is generated from constants, equations, and fixed pseudorandom seeds in `darius_demo/synthetic.py`. The generator does not accept or inspect source datasets. Fictional timestamps begin in 2035; identifiers are `synthetic_city_alpha`, `synthetic_city_beta`, and `synthetic_city_gamma`. Included model artifacts are regenerated only from those CSVs and carry explicit synthetic-only provenance metadata.

Do not add real, sampled, perturbed, anonymised, or pseudonymised municipal rows to this repository. See [privacy and synthetic data](docs/privacy-and-synthetic-data.md).

## Demonstrator configuration

This release uses a compact softmax classifier and a controlled three-client topology to provide a fast and reproducible federated-learning workflow. The experimental configuration, dataset characteristics, evaluation boundaries, and interpretation guidance are documented in [docs/limitations.md](docs/limitations.md).

## License, contributions, and security

The DARIUS Demonstrator is published by DOTSOFT S.A. under the [MIT License](LICENSE).

Contributors can use the public issue and pull-request templates. All proposed
changes are reviewed before acceptance; see
[CONTRIBUTING.md](CONTRIBUTING.md). Report vulnerabilities using the private
process in [SECURITY.md](SECURITY.md), not a public issue.
