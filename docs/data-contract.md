# Data contract

Schema version: `phase7_load_core_plus_lags_v1`. The feature order below is copied from the DARIUS canonical load-classifier contract and is enforced by tests and a SHA-256 order hash.

| # | Column | Unit/range | Synthetic rule |
|---:|---|---|---|
| 1 | `occupancy_rate` | ratio [0,1] | clipped city demand curve + bounded noise |
| 2 | `active_sensors` | count > 0 | fictional capacity × availability |
| 3 | `avg_time_since_change` | seconds > 0 | inverse occupancy-change relation + noise |
| 4 | `avg_prev_state_duration` | seconds > 0 | inverse occupancy-change relation + noise |
| 5 | `dow` | integer 0–6 | artificial timestamp weekday |
| 6 | `time_bucket` | integer 0–95 | 15-minute bucket |
| 7 | `dow_time_bucket` | integer 0–671 | `dow × 96 + time_bucket` |
| 8 | `is_weekend` | 0 or 1 | `dow >= 5` |
| 9 | `is_holiday` | 0 | fixed; no real holiday calendar |
| 10–11 | `hour_sin`, `hour_cos` | [-1,1] | 24-hour cyclic encoding |
| 12–13 | `dow_sin`, `dow_cos` | [-1,1] | seven-day cyclic encoding |
| 14 | `roll_occ_rate_4` | ratio [0,1] | trailing four-row synthetic occupancy mean |
| 15 | `roll_turnover_4` | synthetic count | trailing four-row turnover mean |
| 16 | `roll_occ_rate_12` | ratio [0,1] | trailing 12-row synthetic occupancy mean |
| 17 | `roll_turnover_12` | synthetic count | trailing 12-row turnover mean |
| 18 | `roll_occ_rate_24` | ratio [0,1] | trailing 24-row synthetic occupancy mean |
| 19 | `roll_turnover_24` | synthetic count | trailing 24-row turnover mean |
| 20 | `roll_departure_rate_4` | synthetic count | trailing four-row positive occupancy decrease mean |
| 21 | `occupancy_lag_1` | ratio [0,1] | prior synthetic row |
| 22 | `occupancy_lag_4` | ratio [0,1] | synthetic value one hour earlier |
| 23 | `occupancy_lag_12` | ratio [0,1] | synthetic value three hours earlier |
| 24 | `occupancy_lag_96` | ratio [0,1] | synthetic value one day earlier |

CSV columns are `timestamp`, the 24 ordered features, `load_level_code`, and `load_level`. All feature values must parse as finite numbers. Class mapping is exactly `low=0`, `medium=1`, `high=2`.

Early lags use the first generated synthetic value. Splits are chronological. Preprocessing means and population standard deviations are fitted only on the pooled synthetic training splits. A zero standard deviation is replaced with 1.0.
