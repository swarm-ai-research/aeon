---
id: compute-futures-seed-padding-bug
created: 2026-06-20
type: lesson
links: []
---
# `prototypes/compute-futures/scenario-sweep.mjs` concatenates `YYYYMMDD` with an unpadded index, producing 10-digit seeds beside 9-digit ones

`compute-futures-eda` flags this as a MEDIUM finding: three seeds (2026062010/11/12) are 10-digit vs the other nine 9-digit, inflating the `seed` column to a 25% false-positive IQR outlier rate in every mode. Strategy output is unaffected — just zero-pad the index in the deployer to close the artifact.
