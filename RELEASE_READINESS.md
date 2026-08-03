# Release readiness

Final recommendation: **READY FOR THE FIRST TAGGED RELEASE**.

DOTSOFT S.A. has authorised publication of this controlled demonstrator under
the MIT License at
`https://github.com/DOTSOFT-SA/darius-demonstrator`. The reviewed publication
candidate has been merged into `main`. Private vulnerability reporting is
enabled, and clean public-clone dependency, reproduction, Flower, test, browser,
release-content scan, and npm audit checks have passed. The project now awaits
creation of the `v0.1.0` tag and corresponding GitHub release from the final
verified `main` commit.

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
`https://github.com/DOTSOFT-SA/darius-demonstrator`. The publication candidate
was merged through public PR #1. The initial publication merge commit is
`012ec30bc69647031731311eac5b3aad0b3635e5`. The `v0.1.0` tag will reference
the final verified `main` commit after this readiness update is merged.

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
- Browser `npm test --prefix browser-edge-client`: 2/2 passed on Node 24.15.0.
- Browser `npm run build`: passed with Vite 7.3.6, esbuild 0.28.1, and ONNX Runtime Web 1.26.0. The build emits the required ONNX Runtime `.mjs` loader and WASM runtime into ignored `dist/` output.
- Chrome runtime verification: JSON/ONNX inference reached `Local format parity: PASS`; bounded sensitivity checks at -15%, 0%, and +15% also passed.
- `npm audit`: zero known vulnerabilities in the current locked dependency tree.
- Current-standard networked Flower smoke on 1.32.1: one SuperLink, three fictional-city SuperNodes, a packaged ServerApp/ClientApp, and `flwr run` completed 3/3 rounds in approximately 46 seconds, with three train/evaluation results per round, zero failures, and validated final parameter shapes `[24, 3]` and `[3]`.
- Final release-only filename/content/size scan: passed with the findings above.

## Commands not executed

- No Docker build or complete monorepo suite: outside the minimal candidate and unnecessary for this path.
- No full cross-browser or accessibility audit: Chrome runtime behavior is verified, but Firefox/Safari and formal accessibility testing remain outside this MVP.

## Known limitations

See `docs/limitations.md`. Most importantly: synthetic-only results do not validate municipal performance; the network example lacks production security/privacy controls; and the evidence log is not signed.

The Flower workflow uses the current SuperLink/SuperNode deployment runtime and
Message API. No deprecated `start_server()` or `start_client()` entry point
remains. Local commands intentionally use `--insecure`; TLS, SuperNode
authentication, and deployment hardening remain required outside loopback.

## Completed pre-release gates

1. The complete demonstrator is publicly available in the canonical GitHub repository.
2. GitHub private vulnerability reporting is enabled and monitored by authorised DOTSOFT R&D DARIUS maintainers.
3. Clean public-clone dependency, test, Flower, browser, audit, and reproduction checks passed on 2026-08-03.
4. Version metadata is aligned to `0.1.0`.
5. Publication PR #1 was merged into `main`.

## Remaining release actions

1. Verify the final post-merge `main` commit from a fresh clone.
2. Tag that verified commit as `v0.1.0`.
3. Publish the corresponding GitHub release.

## Question 10 evidence references

| Evidence | Exact reference |
|---|---|
| GitHub URL | `https://github.com/DOTSOFT-SA/darius-demonstrator` |
| Publication PR | `https://github.com/DOTSOFT-SA/darius-demonstrator/pull/1` |
| Initial publication merge | `012ec30bc69647031731311eac5b3aad0b3635e5` |
| License | `MIT License — LICENSE` |
| Release | `v0.1.0 — to be created from the reviewed main-branch merge commit` |
| README | `README.md` |
| Synthetic data | `synthetic-data/generated/` and `synthetic-data/manifests/manifest.json` |
| Contribution process | `CONTRIBUTING.md` |
| Bug template | `.github/ISSUE_TEMPLATE/bug_report.md` |
| Feature template | `.github/ISSUE_TEMPLATE/feature_request.md` |
| Pull-request template | `.github/pull_request_template.md` |
| Reproduction | `docs/reproduction-guide.md` |

The planned release reference is not completed evidence until the `v0.1.0` tag and GitHub release have been published.
