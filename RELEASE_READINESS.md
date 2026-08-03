# DARIUS Demonstrator v0.1.0 release record

Release status: **PUBLISHED**.

DOTSOFT S.A. published the DARIUS Demonstrator under the MIT License through
the canonical public repository:

`https://github.com/DOTSOFT-SA/darius-demonstrator`

The final verified commit
[`13f051b461935db38045b618899e723f1a1e8f48`](https://github.com/DOTSOFT-SA/darius-demonstrator/commit/13f051b461935db38045b618899e723f1a1e8f48)
was tagged as `v0.1.0` and published through the
[official GitHub release](https://github.com/DOTSOFT-SA/darius-demonstrator/releases/tag/v0.1.0)
on 3 August 2026.

Private vulnerability reporting is enabled, and clean public-clone dependency,
reproduction, Flower, test, browser, release-content, and npm audit checks were
completed successfully.

## Scope of this record

This document records the contents and verification status of the exact
`v0.1.0` tagged release.

Documentation-only changes subsequently merged into `main`, including the
approved DARIUS project banner added through
[PR #3](https://github.com/DOTSOFT-SA/darius-demonstrator/pull/3), are not part
of the `v0.1.0` tagged source archive.

## Included component inventory

The `v0.1.0` release contains:

- a Browser Edge Client with JSON and ONNX browser-local inference and bounded sensitivity analysis;
- deterministic three-client federated training and weighted aggregation;
- Flower ServerApp and ClientApp Message API components;
- a SuperLink and three-SuperNode launcher;
- the DARIUS orchestration command and SHA-256 hash-chained evidence;
- three fictional synthetic cities with train, validation, and test CSVs and manifests;
- synthetic-data-derived JSON and ONNX model artifacts;
- installation, architecture, data-contract, privacy, reproduction, limitation, contribution, security, issue, and pull-request documentation.

Detailed design and inventory information is available in
[`docs/release-inventory.md`](docs/release-inventory.md).

## Excluded and sensitive inventory

The `v0.1.0` release excludes:

- ETL city services and their data or configuration;
- municipal datasets and original municipal data rows;
- previously existing source models, reports, evidence, checkpoints, and ONNX files;
- unreviewed legacy brand assets and broader internal user-interface material;
- Postman collections, transfers, archives, internal reports, documents, and notebooks;
- environment values, database state, network captures, and local logs;
- build output, virtual environments, caches, local configuration, and Git history.

The approved project banner subsequently added under
`docs/assets/darius-logo.png` is a documentation-only addition on `main` and is
not contained in the `v0.1.0` tag.

## Licence status

**Resolved.**

The root [`LICENSE`](LICENSE) contains the MIT License with copyright attributed
to DOTSOFT S.A. The project metadata in `pyproject.toml` declares the matching
`MIT` SPDX identifier.

DOTSOFT S.A. authorised publication of the demonstrator under these terms.

## Repository and release status

**Resolved.**

The canonical repository is publicly accessible at:

`https://github.com/DOTSOFT-SA/darius-demonstrator`

The publication candidate was merged through
[PR #1](https://github.com/DOTSOFT-SA/darius-demonstrator/pull/1). The initial
publication merge commit was
`012ec30bc69647031731311eac5b3aad0b3635e5`.

The final release-readiness update was merged through
[PR #2](https://github.com/DOTSOFT-SA/darius-demonstrator/pull/2).

The resulting verified commit
`13f051b461935db38045b618899e723f1a1e8f48` was tagged as `v0.1.0` and published
through the corresponding GitHub release.

## Synthetic-data provenance

All included CSV files are generated independently by
`darius_demo/synthetic.py` from fixed seeds and documented equations.

The generator does not consume an external dataset. It uses fictional city
identifiers and timestamps beginning in 2035. Manifest hashes are recorded in
`synthetic-data/manifests/manifest.json`.

## Synthetic-model provenance

`scripts/reproduce.py` trains the included softmax classifier using the
generated synthetic training splits and exports corresponding JSON and ONNX
representations.

Model provenance is embedded in the JSON and ONNX metadata. The published model
artifacts are regenerated from the included synthetic datasets.

## v0.1.0 release audit summary

The final `v0.1.0` release-folder scan found:

- no credential-like assignments, connection strings, email addresses, absolute user paths, real municipality identifiers, malformed encoding markers, risky environment, log, capture, or archive filenames, reparse points, or files over 5 MiB;
- one binary file: the generated 700-byte `browser-edge-client/public/models/synthetic_softmax.onnx`, whose graph metadata and matching JSON record synthetic-data provenance;
- no vendored dependencies, build output, virtual environments, caches, Git history, or local configuration in the tagged release contents.

Local `node_modules/` and `dist/` directories created during validation are
ignored and are not included in the release.

The broader source audit identified material that remained outside the public
release, including environment files, HAR captures, logs, internal reports,
transfer archives, source model artifacts, and other internal validation
material. These files were not copied into the public repository, and no secret
value was exposed during review.

## Verification

The following checks were completed for the `v0.1.0` release candidate:

- `python fl-orchestrator/orchestrate_demo.py --rounds 3`: passed; the evidence chain was verified; test accuracies were alpha `0.859375`, beta `0.677083`, and gamma `0.682292`;
- two consecutive three-round reproductions produced byte-identical manifest, JSON, and ONNX artifacts;
- `python -m unittest discover -s tests -v`: 7/7 tests passed on Python 3.14.5;
- browser `npm test --prefix browser-edge-client`: 2/2 tests passed on Node.js 24.15.0;
- browser `npm run build --prefix browser-edge-client`: passed with Vite 7.3.6, esbuild 0.28.1, and ONNX Runtime Web 1.26.0;
- Chrome runtime verification reached `Local format parity: PASS`;
- bounded sensitivity checks at `-15%`, `0%`, and `+15%` passed;
- `npm audit` reported zero known vulnerabilities in the locked dependency tree;
- the Flower 1.32.1 network workflow completed 3/3 rounds with one SuperLink, three fictional-city SuperNodes, three train and evaluation results per round, and zero client failures;
- final parameter shapes were validated as `[24, 3]` and `[3]`;
- the final release-only filename, content, and size scan passed;
- the final verification working tree was clean.

The public fresh-clone verification record is available in the
[PR #2 verification comment](https://github.com/DOTSOFT-SA/darius-demonstrator/pull/2#issuecomment-5165231760).

### Reproduced hashes

| Artifact | SHA-256 |
|---|---|
| Manifest | `a0c88657f2699d70345bf6737276d1f4749b77dd8a8e1482f0976cdebbeca5e0` |
| JSON model | `8fe5f9b2883c4c159333ef02c1ea8b234fe63828e9f125556a5e65706ad82a89` |
| ONNX model | `7f10da29646ee961f83d757b9a9861f09b930ac73fbe60ca3fe50bef8e50a965` |

## Verification boundaries

The release verification focused on the published demonstrator workflow.

The following activities were outside this verification path:

- a Docker build and complete internal monorepo test suite;
- a full cross-browser test across Chrome, Firefox, and Safari;
- a formal accessibility audit using assistive technologies.

Chrome runtime behaviour, the documented browser tests, JSON/ONNX parity, the
Flower workflow, deterministic reproduction, and the public release contents
were verified as described above.

## Technical configuration

The experimental configuration and interpretation guidance are documented in
[`docs/limitations.md`](docs/limitations.md).

The Flower workflow uses the current SuperLink/SuperNode deployment runtime and
Message API. No deprecated `start_server()` or `start_client()` entry point is
used.

The documented multi-process commands use local loopback connections. For
communication across separate machines, TLS and authenticated Flower
connections should be configured according to the deployment environment.

## Completed release gates

1. The complete demonstrator was made publicly available in the canonical GitHub repository.
2. GitHub private vulnerability reporting was enabled and assigned to authorised DOTSOFT R&D DARIUS maintainers.
3. Clean public-clone dependency, test, Flower, browser, audit, and reproduction checks passed on 3 August 2026.
4. Version metadata was aligned to `0.1.0`.
5. Publication PR #1 was merged into `main`.
6. Release-readiness PR #2 was merged into `main`.
7. The final release commit was verified from a fresh public clone.

## Completed release actions

1. The final post-merge `main` commit was verified from a fresh public clone.
2. Commit `13f051b461935db38045b618899e723f1a1e8f48` was tagged as `v0.1.0`.
3. The DARIUS Demonstrator v0.1.0 GitHub release was published on 3 August 2026.
4. GitHub-generated ZIP and TAR.GZ source archives were made publicly available through the release page.

## Requirement 10 evidence references

| Evidence | Exact reference |
|---|---|
| Public repository | https://github.com/DOTSOFT-SA/darius-demonstrator |
| Official tagged release | https://github.com/DOTSOFT-SA/darius-demonstrator/releases/tag/v0.1.0 |
| Verified release commit | https://github.com/DOTSOFT-SA/darius-demonstrator/commit/13f051b461935db38045b618899e723f1a1e8f48 |
| Publication PR | https://github.com/DOTSOFT-SA/darius-demonstrator/pull/1 |
| Release-readiness PR | https://github.com/DOTSOFT-SA/darius-demonstrator/pull/2 |
| Final public-clone verification | https://github.com/DOTSOFT-SA/darius-demonstrator/pull/2#issuecomment-5165231760 |
| MIT License | https://github.com/DOTSOFT-SA/darius-demonstrator/blob/v0.1.0/LICENSE |
| Versioned README | https://github.com/DOTSOFT-SA/darius-demonstrator/blob/v0.1.0/README.md |
| Synthetic datasets and documentation | https://github.com/DOTSOFT-SA/darius-demonstrator/tree/v0.1.0/synthetic-data |
| Synthetic-data manifest | https://github.com/DOTSOFT-SA/darius-demonstrator/blob/v0.1.0/synthetic-data/manifests/manifest.json |
| Reproduction guide | https://github.com/DOTSOFT-SA/darius-demonstrator/blob/v0.1.0/docs/reproduction-guide.md |
| Contribution process | https://github.com/DOTSOFT-SA/darius-demonstrator/blob/v0.1.0/CONTRIBUTING.md |
| Public issues | https://github.com/DOTSOFT-SA/darius-demonstrator/issues |
| Public pull requests | https://github.com/DOTSOFT-SA/darius-demonstrator/pulls |

Together, these references provide completed public evidence for the
open-source and participatory-development assessment.
