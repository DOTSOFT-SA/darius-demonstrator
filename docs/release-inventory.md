# Release inventory and design

## Included — critical

| Component | Included scope | Reason |
|---|---|---|
| Browser Edge Client | Minimal Vite/JavaScript client, JSON softmax inference, ONNX Runtime Web inference, bounded what-if, focused tests | Demonstrates local inference without copying production UI or branding assets |
| Federated learning | Shared deterministic local training/FedAvg implementation plus Flower ServerApp, ClientApp, SuperLink, and SuperNode adapters | Reproducible smoke path and genuine current-standard Flower transport path |
| FL orchestration/evidence | Single command, accepted-update events, aggregation events, artifact export, SHA-256 event chain | Makes the evidence flow inspectable and testable |
| Synthetic data | Three fictional non-IID cities, fixed seeds, train/val/test splits, metadata, manifest | Exercises all workflows without municipal input |
| Synthetic model | Regenerated softmax JSON and ONNX artifacts with explicit provenance | Enables both browser-local formats safely |
| Public project files | README, MIT License, contribution/security guidance, issue/PR templates, notices, changelog | Makes post-approval GitHub participation real rather than aspirational |

## Excluded — critical safety or scope decisions

| Source material | Reason excluded |
|---|---|
| All ETL city services and their data/configuration | Coupled to real municipality identifiers, databases, and operational configuration; unnecessary for the demonstrator |
| Existing `DARIUS_Flower_FL/data`, reports, evidence, checkpoints, models, ONNX files | Provenance may involve municipal data or internal validation; publication was not authorised |
| Existing Browser Edge Client models, binaries, brand images, HAR analyzers, dashboards, evidence fixtures | Model/data provenance or third-party asset rights are not established; broader UI is not required |
| Existing FL Orchestrator persisted data and real-city demo fixtures | Contains real-city identifiers and an internal operational design beyond MVP scope |
| Postman collections, transfers, archives, reports, documents, notebooks | Internal endpoints/evidence, size, duplication, or ambiguous disclosure scope |
| `.env*` values, caches, virtual environments, logs, build output, `.git` | Secrets/local state, noise, size, or history disclosure risk |

## Sensitive or ambiguous source observations

- The source worktree contains tracked example environment files and an untracked Flower `.env.local`; none were copied.
- Source reports, transfer archives, local logs, model binaries, and real-city identifiers exist; none were copied.
- Existing source edits and untracked files were preserved.
- The source secret scan was category-based and did not expose values. Final release-folder scanning is recorded in `RELEASE_READINESS.md`.

## License status

The demonstrator is licensed under the MIT License, with copyright attributed
to DOTSOFT S.A. This resolves the explicit-license requirement for the
candidate. DOTSOFT S.A. has authorised publication at
`https://github.com/DOTSOFT-SA/darius-demonstrator`.

## Public directory structure

```text
darius-demonstrator/
  .github/                 issue and pull-request templates
  browser-edge-client/     local JSON/ONNX demo
  darius_demo/             shared schema/training/evidence code
  docs/                    architecture, contracts, privacy, reproduction, limits
  evidence/                reproducible generated run summaries
  fl-orchestrator/         one-command controlled workflow
  darius_fl_app/           Flower ServerApp and ClientApp
  flower-federated-learning/ SuperLink/SuperNode launcher
  scripts/                 end-to-end reproduction entry point
  synthetic-data/          generator, generated splits, manifests
  tests/                   public package verification
```
