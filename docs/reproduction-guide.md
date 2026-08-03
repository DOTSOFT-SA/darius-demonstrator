# Reproduction guide

Use a clean checkout of the canonical public repository.

1. Create and activate a Python virtual environment.
2. Run `python -m pip install -r requirements.txt`.
3. Run `python scripts/reproduce.py --rounds 3`.
4. Run `python -m unittest discover -s tests -v`.
5. Run `npm ci --prefix browser-edge-client`.
6. Run `npm test --prefix browser-edge-client`.
7. Run `npm run build --prefix browser-edge-client`.
8. Run `npm run dev --prefix browser-edge-client`. Confirm the page automatically reports `Local format parity: PASS`, then manually rerun at -15%, 0%, and +15% and confirm both result panels change together.

For the true multi-process Flower transport path, install
`flower-federated-learning/requirements.txt`, then run
`python flower-federated-learning/run_demo.py --rounds 3`. The launcher starts
one SuperLink, three separate SuperNodes, and submits the Flower App through
`flwr run`. Confirm it prints `FLOWER DEMO COMPLETE` and that
`evidence/flower_network_result.json` reports the
`SuperLink/SuperNode` runtime, three accepted clients, and zero failures for the
final round. The manual current-standard commands in `README.md` remain
available for inspecting each process independently.

Review `synthetic-data/manifests/manifest.json`, model provenance fields, and the evidence hash chain. Then inspect `RELEASE_READINESS.md`; do not infer readiness from passing tests alone.

The manifest and artifact hashes are evidence for a particular working tree. A
release tag/commit should be recorded only after the MIT License, publication
authorisation, final security details, and clean-clone results are committed.
