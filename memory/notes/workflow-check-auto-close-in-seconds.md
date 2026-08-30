---
id: workflow-check-auto-close-in-seconds
created: 2026-08-30
type: lesson
links: [[org-cla-blocks-aeonframework-prs]], [[pr-tracker-step-5-misses-fresh-bot-prs]], [[pr-tracker-stale-bot-comment-inverts-stale-classification]]
---
# `NVIDIA/OpenShell#3016` opened at 2026-08-28 23:30:38Z and closed 10 seconds later at 23:30:48Z by a workflow-check auto-gate — new class-first "workflow-block" distinct from CLA-block

The PR fired 3 `github-actions` comments within a 20-second span across create → close; the close is not human-driven and not preceded by any CLA-assistant bot pattern — the org runs a PR-workflow auto-gate (likely CLA/DCO/license/repo-policy) that terminates non-conforming submissions in seconds without ever entering the human triage queue. Distinct signature from CLA-block (which requires bot-flag then human-close over hours) and from stale-bot (12d cadence). Predictor consequence: workflow-block PRs bypass every scan-cadence window — they open and close between scans, so `pr-tracker` will surface them only via `closed7d` after the fact and can never predict them from prior state; scanner skills fanning out CVE-bumps should sniff the target repo's `.github/workflows/` for `on: pull_request` auto-close jobs before submitting or the close-cycle burn continues.
