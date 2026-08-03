# Release inventory and design

This inventory describes the public DARIUS Demonstrator and records the
relationship between the tagged `v0.1.0` release and later documentation-only
updates on `main`.

## Included — critical

| Component | Included scope | Reason |
|---|---|---|
| Browser Edge Client | Minimal Vite/JavaScript client, JSON softmax inference, ONNX Runtime Web inference, bounded what-if analysis, and focused tests | Demonstrates local browser inference through a small, inspectable public interface |
| Federated learning | Shared deterministic local-training and weighted-FedAvg implementation plus Flower ServerApp, ClientApp, SuperLink, and SuperNode adapters | Provides a reproducible local workflow and a current-standard Flower multi-process workflow |
| FL orchestration and evidence | Single orchestration command, accepted-update events, aggregation events, artifact export, and SHA-256 event chain | Makes the workflow and evidence generation inspectable and testable |
| Synthetic data | Three fictional non-IID cities, fixed seeds, train/validation/test splits, metadata, and deterministic manifest | Exercises the workflow through independently generated synthetic datasets |
| Synthetic model | Regenerated softmax JSON and ONNX artifacts with explicit synthetic-data provenance | Enables reproducible inference through both browser-local formats |
| Public project files | README, MIT License, contribution and security guidance, issue and pull-request templates, notices, changelog, architecture, data-contract, privacy, limitation, and reproduction documentation | Supports external inspection, reproduction, issue reporting, and proposed improvements |
| Approved project banner | `docs/assets/darius-logo.png`, added to `main` after the `v0.1.0` release | Presents the approved DARIUS, dAIEDGE, European Union funding, and DOTSOFT project identities |

The approved project banner was added through
[PR #3](https://github.com/DOTSOFT-SA/darius-demonstrator/pull/3) after the
`v0.1.0` release. It is therefore available on current `main` but is not part of
the tagged `v0.1.0` source archive.

## Excluded — critical safety or scope decisions

| Source material | Reason excluded |
|---|---|
| ETL city services and their data or configuration | Coupled to municipality identifiers, databases, and operational configuration that are not required for the public demonstrator |
| Existing `DARIUS_Flower_FL/data`, reports, evidence, checkpoints, models, and ONNX files | Their provenance may involve municipal data or internal validation material, and they were not included in the authorised publication scope |
| Existing unreviewed Browser Edge Client models, binaries, legacy brand images, HAR analyzers, dashboards, and evidence fixtures | Model and data provenance or asset reuse rights were not established for the public release, and the broader interface was not required for the demonstrator |
| Existing FL Orchestrator persisted data and real-city demonstration fixtures | Contains real-city identifiers and internal workflow material beyond the public demonstrator scope |
| Postman collections, transfers, archives, internal reports, documents, and notebooks | May contain internal endpoints, evidence, duplicated material, or content outside the authorised publication scope |
| Environment values, caches, virtual environments, logs, build output, and Git history | Contains local state, generated output, environment-specific information, or unnecessary repository history |

The approved public banner under `docs/assets/darius-logo.png` is distinct from
the unreviewed legacy brand images excluded from the original source worktree.

## Sensitive or ambiguous source observations

- The broader source worktree contained tracked example environment files and an untracked Flower `.env.local`; these were not copied into the public demonstrator.
- Internal source reports, transfer archives, logs, model binaries, and real-city identifiers were not copied into the public demonstrator.
- Existing edits and untracked files in the source worktree were preserved during preparation of the public release.
- The source secret scan was category-based and did not expose candidate values.
- Final `v0.1.0` release-folder scanning and verification are recorded in [`RELEASE_READINESS.md`](../RELEASE_READINESS.md).

## Licence status

The DARIUS Demonstrator is published under the MIT License, with copyright
attributed to DOTSOFT S.A.

The official `v0.1.0` release is available at:

`https://github.com/DOTSOFT-SA/darius-demonstrator/releases/tag/v0.1.0`

DOTSOFT S.A. authorised publication through the canonical repository:

`https://github.com/DOTSOFT-SA/darius-demonstrator`

The approved project banner and the names, emblems, and visual identities shown
within it remain subject to their applicable project and brand guidelines.

## Public directory structure

```text
darius-demonstrator/
  .github/                   issue and pull-request templates
  browser-edge-client/       local JSON and ONNX inference demonstrator
  darius_demo/               shared schema, training, aggregation, export, and evidence logic
  docs/                      architecture, contracts, privacy, reproduction, limits, and assets
    assets/                  approved public project banner on current main
  evidence/                  reproducible generated run summaries
  fl-orchestrator/           one-command deterministic workflow
  darius_fl_app/             Flower ServerApp and ClientApp
  flower-federated-learning/ SuperLink and SuperNode launcher
  scripts/                   end-to-end reproduction entry point
  synthetic-data/            generator, generated splits, metadata, and manifests
  tests/                     public package verification
