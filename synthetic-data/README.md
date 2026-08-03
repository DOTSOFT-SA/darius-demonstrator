# Synthetic data

All data here is demonstration-only and independently generated. The generator takes no source dataset argument and does not sample, perturb, anonymise, or approximate municipal rows.

## Reproduce

From the repository root:

```bash
python synthetic-data/generator/generate.py
```

The command uses Python's deterministic `random.Random` implementation, emits UTF-8 CSV with LF line endings, and records SHA-256 hashes in `manifests/manifest.json`.

## Fictional environments

| City | Seed | Capacity constant | Distribution intent |
|---|---:|---:|---|
| `synthetic_city_alpha` | 104729 | 160 | stronger morning load |
| `synthetic_city_beta` | 130363 | 240 | higher base and evening load |
| `synthetic_city_gamma` | 155921 | 110 | two balanced, sharper peaks |

Each city has 672 train, 192 validation, and 192 test rows. Rows are chronological 15-minute intervals beginning at the clearly artificial UTC date `2035-01-01`. Every split contains all three target classes. Different base levels, peaks, capacities, phases, and seeds deliberately create non-IID client distributions.

## Generation rules

Occupancy is the clipped sum of a city-specific base, Gaussian morning and evening peaks, a sinusoidal daily component, a weekend multiplier, and bounded independent noise. `active_sensors` is a city-specific fictional capacity with small availability noise. Duration fields are inverse functions of occupancy change plus bounded noise. Calendar and trigonometric features derive only from the artificial timestamp. Rolling and lag fields derive only from earlier synthetic occupancy/turnover values.

The label predicts synthetic occupancy one hour (four 15-minute rows) ahead:

- `low` / 0: future occupancy below 0.60;
- `medium` / 1: future occupancy from 0.60 to below 0.80;
- `high` / 2: future occupancy at least 0.80.

Full column units, order, and constraints are in [the data contract](../docs/data-contract.md). The implementation in `darius_demo/synthetic.py` is authoritative.
