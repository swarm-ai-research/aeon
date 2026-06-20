---
id: oauth-outage-zero-token-signature
created: 2026-06-20
type: lesson
links: [[monitor-monitored-coupling]], [[issues/ISS-001]]
---
# A missing CLAUDE_CODE_OAUTH_TOKEN produces a zero-token result_json with `total_cost_usd:0`

Symptom: every cron-run row in `memory/cron-state.json` carries `"total_cost_usd":0,"usage":{"input_tokens":0,"output_tokens":0}` and dies in <1s — the CLI never reached the API. Whenever this pattern appears fleet-wide, suspect the auth secret first; the recovery signal is the first batch with non-zero `output_tokens`.
