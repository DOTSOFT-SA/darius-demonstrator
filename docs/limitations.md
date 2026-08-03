# Limitations and non-claims

- Synthetic distributions cannot validate performance on real municipal data.
- The softmax model is intentionally small and is not a production forecasting system.
- Three controlled clients do not represent realistic federation scale, churn, adversaries, or network conditions.
- Weighted FedAvg is visible and reproducible but has no secure aggregation or differential privacy.
- Loopback Flower transport is unencrypted and unauthenticated in this example.
- The evidence log is tamper-evident only while a trusted final hash is retained; it is not a signed audit record.
- Browser-local what-if output is bounded sensitivity analysis, not causal or policy-impact evidence.
- No demographic attributes exist, so no demographic-fairness claim is made.
- No legal, regulatory, security, privacy, production-readiness, or formal WCAG certification is claimed.
- Dependency ranges need a locked, clean-environment review before a public release.
