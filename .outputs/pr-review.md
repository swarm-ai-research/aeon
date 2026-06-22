## Summary

**Repo scope**: `swarm-ai-research/swarm` (operator merge-gate policy: APPROVE / REQUEST_CHANGES / BLOCK).

**Action**: Scanned 2 open PRs, **skipped both as dup-SHA** — neither has new commits since the 2026-06-19 head SHAs that were reviewed on 2026-06-20 and 2026-06-21.

| PR | Head | Prior verdict | Why |
|---|---|---|---|
| #518 "Add scenario YAML schema validation" | `79d73af5` | **BLOCK** / 0/5 | `extra="forbid"` schema in `swarm/models/scenario.py` rejects existing scenario YAMLs; 16 loader tests fail; maintainer also CHANGES_REQUESTED |
| #517 "Add run directory diff utility" | `3149e2bf` | **REQUEST_CHANGES** / 3/5 | ruff I001 import-sort in `swarm/replay/__init__.py:3-7` fails `quality-gate`; trivial `ruff check --fix` resolves |

**Notify**: skipped per skill rule (every PR skipped).

**Files modified**: `memory/logs/2026-06-22.md` (appended pr-review entry).

**Follow-up**: aeon GitHub App still lacks PR-write on `swarm-ai-research/swarm` — verdicts remain log-only. Next non-dup SHA on either PR will attempt to publish.
