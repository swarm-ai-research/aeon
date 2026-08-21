# Plan — 2026-08-21

**Today's one thing:** Diagnose why the textbook auto-merge candidate PR #26 (dependabot `actions/checkout` bump) is not mergeable — GitHub reports `mergeable: UNKNOWN` and 1/5 status checks failing (`ShellCheck` FAILURE from 2026-08-17T01:09:55Z, workflow `Lint`). This is the specific `app/github-actions`-merge blocker hiding behind the streak-13 queue-merge stalemate; fix or waive the ShellCheck lint and #26 lands the same class as merged #8.

## Ranked

1. **Investigate PR #26 ShellCheck FAILURE and land #26 (or #41)** — streak 13 → 14, ESCALATED from restatement. Day-15 of stalled `app/github-actions` merge flow since 2026-08-07 (≈344h+ no merge, last merged #8 dependabot actions/checkout — the SAME class). Queue is now 26 open aeon-repo PRs (+#41 notegraph "graph refreshed 307n/3156e/0b" opened 05:10Z today; +#42 suggest-edges opened 05:47Z today). The signal is now specific, not general: `gh pr view 26 --json statusCheckRollup` shows ShellCheck failed (workflow `Lint`, `runs/31984128476/job/95256043957`) while TypeScript (a2a-server/mcp-server/dashboard) and compute-futures tests all PASS. Concrete action: read the ShellCheck job log, either fix the offending shell file or waive the check on dependabot-authored PRs. #41 is also merge-eligible (notegraph head, 16-file diff heavy on `dashboard/outputs/` + `docs/notegraph.*` regens, no status checks required per `statusCheckRollup: []`). Serves the aeon-repo merge-flow proof — the single highest-leverage goal we have.

2. **Ship `enabled: false` on `aeon.yml:188` for agi-tracker** — streak 5 → 6, deadline TIGHTENS from 4d → **3d out** (8th silent-Mon fires 2026-08-24T13:00Z). Any PR opened today has 3 workdays to clear review + auto-merge before the 8th no-op runs; the runway is closing. Alt path (a) restore `skills/agi-tracker/SKILL.md` matching [[agi-tracker]] MOC's weekly frontier-agent scoring shape — higher-leverage but not tractable in a day; alt (b) `enabled: false` is the lower-friction merge — pulls ms-02 from 47/50 → 46/50 but stops the silent-run cadence. The two-lever framing per [[pr-creation-toggle-is-distinct-from-merge-capability]] applies: creation is viable, merge is what's unproven — landing this PR *is* also a merge-flow proof (rank-1 supported by rank-2 in the same stroke).

3. **Patch `stale-content-pr-sweeper` SKILL.md `ALLOWED_AUTHORS` + TRACKED-prefix drift** — streak 14 → 15, still rank-holding. Yesterday's sweeper run confirmed the branch-drift hypothesis: 8 candidates (4 notegraph + 4 suggest-edges) all `app/github-actions` fail the hardcoded `{"aeonframework"}` allowlist; separately `compute-macro/*` (#33/#23) and `skill-graph/*` (#34/#25) never even match TRACKED because branch prefixes diverge from skill names ([[stale-content-pr-sweeper-tracked-prefix-drift]]). Under a patched allowlist, today's sweeper would close 6 stale PRs (notegraph #32/#35/#36 superseded by #41; suggest-edges #22/#37/#38/#40 superseded by #42). Bundle both fixes (allowlist + TRACKED-prefix aliases) in one PR — small, high-leverage, and if rank-1 ships, this second PR further proves the flow.

## Holding / watching

- **pr-tracker 57d-overdue batch patch** — bundled 11-item fix (items a-k in MEMORY.md line 55). Item (d) hash-dedup guard urgency partially masked by newly-confirmed queue-level [[notify-has-hash-dedup-queue-layer]] but SKILL-level guard still needed. Promotion trigger: any new pr-tracker cluster whose payload duplication *isn't* caught by the queue-level dedup, OR any operator ping about noisy pr-tracker notifications.
- **ISS-006 messages.yml multi-pocket rewrite** — Day-19. Today's 06:00–07:30Z window (odd DOM) expects 2 in-window skills (planner + compute-futures-eda). Promotion trigger: consecutive-day batch-outage or a new pocket-slot dead-zone.
- **docs/status.md snapshot-rebase gate** — 35 days past urgency (23rd regen unchanged; today's heartbeat pending). Promotion trigger: heartbeat's regen count crosses 25 OR operator raises the churn as noise.
- **watched-repos.md populate-or-disable** — streak-15 chronic, six skills short-circuiting daily (code-health, issue-triage, github-monitor, changelog, weekly-shiplog, repo-revive). Fix path binary; promotion trigger: operator decision on the populate-vs-disable lever.
- **suggest-edges templated-corpus pre-filter** — streak 13. Class continues per [[suggest-edges-cluster-exhaustion-rotates-not-terminates]]. Today's #42 has the same signature as #40/#38/#37. Promotion trigger: cluster jumps outside `gitlawb-compute-futures-proofs/` OR PR count reaches 6.
- **swarm-repo App-write permission gap** — 43/39 counter (pr-review/pr-triage). Distinct from PR-creation toggle. Promotion trigger: gap remains after aeon-repo merge flow is proven (i.e., isolates it from the local-fleet issue).

## Fleet note

Steady: 0 broken · 0 in-flight · 38 DEGRADED (ISS-001 residue Day-63) · 4 truly HEALTHY (agi-tracker, config-validator, swarm-safety-eval, weekly-shiplog) · 2 NO_DATA (ai-framework-watch, run-frequency-guard, 45th silent day) · 18 open ISS · 26 open aeon PRs (0 merged in ~344h+). Cleanest morning again — notegraph 05:03Z → 05:10Z (7m, well under threshold), suggest-edges 05:47Z → 05:49Z (2m).

## Source footer

- Local reads: `memory/MEMORY.md` (65 lines) · `memory/cron-state.json` (42 skills) · `memory/issues/INDEX.md` (18 open / 2 resolved) · last 2d `memory/logs/` (08-20 + 08-21 through suggest-edges) · `memory/state/planner-state.json` (last_run 2026-08-20T06:30Z, top_priority streak 12, 9 tracked streaks).
- External: `gh pr list --state open` → 26 rows (+#41 notegraph 05:10Z, +#42 suggest-edges 05:57Z today) · `gh pr view 26/39/41` all `mergeable: UNKNOWN, state: OPEN`; #26 shows 4/5 checks pass + ShellCheck FAILURE (workflow `Lint`, job `95256043957`) · `gh issue list --state open` → 0.
- `soul/` absent → clear-direct first-person tone. `${var}` empty → plan-only, no dispatch.
- Fourth consecutive day at same top-3 ranking; rank-1 ESCALATED from "merge a PR" (streak-12 restatement) to "diagnose the specific ShellCheck FAILURE blocking the textbook auto-merge class" (concrete unblock) per stuck-goal escalation rule.
