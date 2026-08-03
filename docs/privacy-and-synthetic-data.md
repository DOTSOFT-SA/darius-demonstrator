# Privacy and synthetic-data design

The release boundary is intentionally narrow:

- Generation starts from documented constants, equations, fictional timestamps, and fixed seeds.
- The generator has no input-data option and no connection code.
- No ETL service, database adapter, internal report, network capture, real-city identifier, municipal model, or source dataset is included.
- Synthetic city distributions are designed, not estimated from municipal rows.
- Model artifacts are overwritten by `scripts/reproduce.py` using only included synthetic train splits.
- Artifact metadata states `demonstration_only` and `synthetic-only` provenance.

These controls support inspectability; they do not establish anonymous-data status, GDPR compliance, or safety for arbitrary future contributions. A maintainer must review every added dataset and binary before merging it.

Prohibited contributions include real municipal rows, samples, extracts, row-level transformations, pseudonymised records, credentials, internal URLs, logs, HAR files, database dumps, and models without documented synthetic-only provenance.
