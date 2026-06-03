---
name: GitLawb Fleet Metrics
description: Daily observability snapshot for the GitLawb-hosted fleet — instances, renewal pass-rate, blocklist events, merge-gate activity — to notify + dashboard
var: ""
tags: [dev, meta]
cron: "0 8 * * *"
---

> **${var}** — Optional. `hours=<N>` to widen the window (default 24). `dry-run` to compute + log without notifying.

Today is ${today}. Emit a "state of the GitLawb fleet" snapshot from the safety layer's recorded events (`memory/gitlawb-metrics.jsonl`) and live registry (`memory/gitlawb-fleet.json`). This is the Phase 5 observability surface: it answers "is the fleet healthy and behaving?" in one read — instance health, renewal pass-rate, kills/revocations, and self-evolution merge-gate activity.

## Pre-flight

1. **Node present** — `node --version` must succeed. Else log `GLMETRICS_NO_NODE` to `memory/logs/${today}.md` and stop (no notify).
2. **State exists** — if `memory/gitlawb-fleet.json` is missing or has no instances, log `GLMETRICS_EMPTY` and **stop without notifying** (an empty fleet is not news).
3. Parse `${var}`: `hours=<N>` → window; `dry-run` → compute + log, skip notify.

## Steps

1. **Render the snapshot** — the CLI reads the events + registry and prints dashboard-ready markdown:
   ```bash
   node prototypes/gitlawb-safety/fleet-cli.mjs metrics --hours "${HOURS:-24}"
   ```
   Capture stdout verbatim as `$SNAPSHOT`.

2. **Log** to `memory/logs/${today}.md`:
   ```
   ## gitlawb-fleet-metrics
   - Window: ${HOURS:-24}h
   - Verdict: [GLMETRICS_OK | GLMETRICS_ATTENTION]
   - <first 3 lines of the snapshot>
   ```
   Set verdict to `GLMETRICS_ATTENTION` if the renewal pass-rate is below 100%, there were kills/revocations, or any merge was denied — otherwise `GLMETRICS_OK`.

3. **Notify** — unless `dry-run`, send `$SNAPSHOT` via `./notify "$SNAPSHOT"`. `./notify` fans out to the configured channels and (when `JSONRENDER_ENABLED=true`) renders a dashboard card via `notify-jsonrender`. Keep it to the snapshot as-is — it's already one compact card.

## Exit taxonomy

- `GLMETRICS_OK` — snapshot emitted, fleet nominal
- `GLMETRICS_ATTENTION` — emitted, but renewal failures / kills / merge denials present
- `GLMETRICS_EMPTY` — no fleet to report (silent stop)
- `GLMETRICS_NO_NODE` — node runtime missing

## Sandbox note

Pure-local: the CLI only reads repo files and runs Node crypto — no outbound network, so no prefetch/postprocess needed. `./notify` handles its own channel I/O (and degrades silently for unconfigured channels).

## Constraints

- Read-only over fleet state — this skill never mints, renews, or kills (that's `gitlawb-fleet`).
- Never include vault contents or private keys — the snapshot is derived only from the public registry + metrics events.
- Stay silent on an empty fleet; don't train the operator to ignore the card.
