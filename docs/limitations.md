# Technical scope and interpretation

The following points describe the experimental configuration and provide
guidance for interpreting the demonstrator results.

- The included datasets use controlled synthetic distributions designed for reproducible experimentation. Evaluation with municipal datasets requires a separate, appropriately governed validation exercise.
- The compact softmax classifier is selected for inspectability, fast execution, and deterministic reproduction of the complete workflow.
- The three-client topology provides a focused multi-client federated-learning example. Larger federations may introduce additional scale, availability, churn, adversarial, and network considerations.
- Weighted FedAvg provides a visible and reproducible aggregation baseline. Secure aggregation and differential-privacy mechanisms can be evaluated as separate extensions.
- The documented Flower multi-process workflow uses local loopback connections. Cross-machine environments should configure TLS and authenticated Flower connections.
- The evidence log uses a SHA-256 hash chain. Its integrity depends on retaining and independently recording the trusted final hash.
- The browser-local what-if control performs bounded sensitivity analysis by varying selected occupancy-history features and displaying the corresponding model response.
- The synthetic datasets do not include demographic attributes. Evaluating demographic fairness would require an appropriate dataset, evaluation protocol, and governance basis.
- Legal, regulatory, security, privacy, and accessibility assessments depend on the intended deployment environment and should be conducted separately for that environment.
- The `v0.1.0` dependency set underwent the documented clean-environment and locked-browser-dependency review. Later dependency changes require renewed licence, compatibility, and vulnerability review before a subsequent release.

For the exact `v0.1.0` verification record, see
[`RELEASE_READINESS.md`](../RELEASE_READINESS.md).

For installation and clean-room reproduction instructions, see
[`docs/reproduction-guide.md`](reproduction-guide.md).
