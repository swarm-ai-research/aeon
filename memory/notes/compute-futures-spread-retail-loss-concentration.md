---
id: compute-futures-spread-retail-loss-concentration
created: 2026-08-11
type: pattern
links: [[compute-futures-12-seed-sample-too-small]], [[compute-futures-eda-wallet-sum-pnl-correlations-are-float-dust]]
---
# In compute-futures spread mode, top-5 losses concentrate 100% in the retail role across ≥4 consecutive filed runs

Across the 4-consecutive filed-run window ending 2026-08-10, every top-5 spread-mode loss was booked by the retail role — deepest at seed 202608109 (−$20,016). The pattern meets the 2026-08-08 promotion criterion (n=4 filed runs sustained) and is distinct from the tie-based outlier artifacts covered by [[compute-futures-12-seed-sample-too-small]], since role-share is a categorical property independent of IQR-fence sample size. Next step for the scenario-sweep runner: surface role-share on the loss tail as a first-class finding (not a per-seed anomaly) and flag when it drops below 100% as the regime shift.
