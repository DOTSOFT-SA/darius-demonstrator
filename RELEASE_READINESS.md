# Release readiness

Final recommendation: **NOT READY FOR THE FIRST TAGGED RELEASE**.

DOTSOFT S.A. has authorised publication of this controlled candidate under the
MIT License at
`https://github.com/DOTSOFT-SA/darius-demonstrator`. Technical verification
has passed locally. The complete candidate must still be committed to the
public repository, its security reporting channel configured, and a clean
public-clone reproduction completed before tagging.

## Included component inventory

- Minimal Browser Edge Client with JSON and ONNX browser-local inference and bounded sensitivity.
- Deterministic three-client federated training and weighted aggregation.
- Flower ServerApp/ClientApp Message API components and SuperLink/SuperNode launcher.
- DARIUS orchestration command and SHA-256 hash-chained evidence.
- Three fictional synthetic cities with train/validation/test CSVs and manifests.
- Synthetic-only JSON and ONNX model artifacts.
- Installation, architecture, data contract, privacy, reproduction, limitations, contribution, security, issue, and pull-request documentation.

Detailed design and exclusions: `docs/release-inventory.md`.

## Excluded/sensitive inventory

No ETL services, municipal datasets, original data rows, existing source models, internal reports/evidence, transfers/archives, brand assets, Postman files, environment values, database state, network captures, logs, build output, virtual environments, caches, or Git history are included.

## License status

**Resolved for this candidate.** The root `LICENSE` contains the MIT License,
copyright 2026 DOTSOFT S.A., and `pyproject.toml` declares the matching `MIT`
SPDX identifier. DOTSOFT S.A. has authorised publication under these terms.

## Repository status

**Resolved.** The canonical repository is public at
`https://github.com/DOTSOFT-SA/darius-demonstrator`. The final release evidence
must reference the commit containing this complete candidate rather than the
initial license-only commit.

## Synthetic-data provenance

All CSVs are generated independently by `darius_demo/synthetic.py` from fixed seeds and documented equations. The generator consumes no real dataset. Fictional identifiers and 2035 timestamps are used. Manifest hashes are in `synthetic-data/manifests/manifest.json`.

## Synthetic-model provenance

`scripts/reproduce.py` trains the included softmax classifier exclusively on the generated synthetic training splits, then exports JSON and ONNX. Both artifacts are demonstration-only; provenance is embedded in JSON and ONNX metadata. No pre-existing model was copied.

## Secret/privacy audit summary

The final release-folder scan found:

- no credential-like assignments, connection strings, email addresses, absolute user paths, real municipality identifiers, malformed encoding markers, risky environment/log/capture/archive filenames, reparse points, or files over 5 MiB;
- one binary: the 700-byte generated `browser-edge-client/public/models/synthetic_softmax.onnx`, whose graph metadata and matching JSON declare synthetic-only provenance;
- no vendored dependencies, build output, virtual environments, caches, Git history, or local configuration in the intended Git release set. Local `node_modules/` and `dist/` directories created during validation are ignored and must not be added or manually packaged.

The broader source audit identified material that must remain excluded: `DARIUS_Flower_FL/.env.local` and example environment files; HAR captures under `DARIUS_Flower_FL/reports/`; logs under `Browser_Edge_Client/`, `Occupancy_rate_service/`, and `.tmp/`; and archives under `documents/`, `transfer/`, `DARIUS_Flower_FL/reports/`, and `.tmp/`. Credential-pattern scanning did not identify a candidate value. These source files were not copied, and no secret value was exposed during review.

## Verification

- `python fl-orchestrator/orchestrate_demo.py --rounds 3`: passed; evidence chain verified; test accuracies alpha 0.859375, beta 0.677083, gamma 0.682292.
- Two consecutive three-round reproductions: byte-identical manifest, JSON model, and ONNX model. SHA-256: manifest `a0c88657f2699d70345bf6737276d1f4749b77dd8a8e1482f0976cdebbeca5e0`; JSON `8fe5f9b2883c4c159333ef02c1ea8b234fe63828e9f125556a5e65706ad82a89`; ONNX `7f10da29646ee961f83d757b9a9861f09b930ac73fbe60ca3fe50bef8e50a965`.
- `python -m unittest discover -s tests -v`: 7/7 passed on Python 3.14.5, including per-split class support, finite values, deterministic regeneration, contract order, evidence integrity, provenance, and ONNX Runtime parity.
- Browser `node --test --test-isolation=none tests/inference.test.mjs`: 2/2 passed on Node 24.15.0.
- Browser `npm run build`: passed with Vite 7.3.3 and ONNX Runtime Web 1.26.0. The build emits the required ONNX Runtime `.mjs` loader and 26 MB WASM runtime into ignored `dist/` output.
- Headless Chrome runtime smoke: automatic JSON/ONNX inference reached `Local format parity: PASS` with maximum probability difference `1.65e-8`; a +15% bounded sensitivity rerun changed the probabilities and passed again with maximum difference `1.79e-8`.
- `npm audit`: zero known vulnerabilities in the current locked dependency tree.
- Current-standard networked Flower smoke on 1.32.1: one SuperLink, three fictional-city SuperNodes, a packaged ServerApp/ClientApp, and `flwr run` completed 3/3 rounds in approximately 46 seconds, with three train/evaluation results per round, zero failures, and validated final parameter shapes `[24, 3]` and `[3]`.
- Final release-only filename/content/size scan: passed with the findings above.

## Commands not executed

- No Docker build or complete monorepo suite: outside the minimal candidate and unnecessary for this path.
- No full cross-browser or accessibility audit: Chrome runtime behavior is verified, but Firefox/Safari and formal accessibility testing remain outside this MVP.
- No separate clean-machine clone: `npm ci`, the browser build, Python tests, and Chrome runtime passed in the release folder; a final clean-machine run remains appropriate immediately before tagging.

## Known limitations

See `docs/limitations.md`. Most importantly: synthetic-only results do not validate municipal performance; the network example lacks production security/privacy controls; and the evidence log is not signed.

The Flower workflow uses the current SuperLink/SuperNode deployment runtime and
Message API. No deprecated `start_server()` or `start_client()` entry point
remains. Local commands intentionally use `--insecure`; TLS, SuperNode
authentication, and deployment hardening remain required outside loopback.

## Unresolved blockers

1. Commit this complete candidate to the public repository's default branch.
2. Name a monitored DOTSOFT security maintainer and enable GitHub private vulnerability reporting.
3. Run and record a clean public-clone dependency/license review and reproduction.
4. Record the final commit SHA, create the version tag, and publish the GitHub release.

## Question 10 evidence references

| Evidence | Exact reference |
|---|---|
| GitHub URL | `https://github.com/DOTSOFT-SA/darius-demonstrator` |
| License | `MIT License — LICENSE` |
| Release | `<RELEASE_TAG_OR_COMMIT — NOT YET CREATED>` |
| README | `README.md` |
| Synthetic data | `synthetic-data/generated/` and `synthetic-data/manifests/manifest.json` |
| Contribution process | `CONTRIBUTING.md` |
| Bug template | `.github/ISSUE_TEMPLATE/bug_report.md` |
| Feature template | `.github/ISSUE_TEMPLATE/feature_request.md` |
| Pull-request template | `.github/pull_request_template.md` |
| Reproduction | `docs/reproduction-guide.md` |

Do not insert these placeholders into a validation report as if they were completed evidence.
