---
id: monitor-monitored-coupling
created: 2026-06-20
type: lesson
links: [[oauth-outage-zero-token-signature]], [[issues/ISS-001]]
---
# Monitoring skills that share a dependency with the monitored fleet cannot detect outages of that dependency

During the 2026-06-06 → 2026-06-20 OAuth outage every monitoring skill (`skill-health`, `heartbeat`, `batch-health`, `skill-evals`, `skill-repair`, `memory-flush`) was itself failing for the same reason and so couldn't fire an alert. The fix is an out-of-band canary: either a pre-flight credential check in `aeon.yml` or a separate-account pinger that watches "zero Aeon skills succeeded in last 6h".
