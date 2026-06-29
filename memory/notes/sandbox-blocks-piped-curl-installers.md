---
id: sandbox-blocks-piped-curl-installers
created: 2026-06-21
type: lesson
links: [[oauth-outage-zero-token-signature]]
---
# The Aeon sandbox blocks `bash <(curl …)` and direct exec of `~/.local/bin/*`, so audit skills that bootstrap their own scanner degrade to hand-rolled fallbacks

Observed on 2026-06-21 when `workflow-security-audit` tried to install/run `zizmor` and `actionlint`: both bootstrap paths failed inside the sandbox (the curl-pipe install is blocked, and pre-installed binaries under `~/.local/bin` aren't on PATH). The skill exited `WORKFLOW_AUDIT_TOOL_DEGRADED` with hand-rolled regex coverage only. New audit-style skills should either ship the scanner via a prefetch script run before Claude (same pattern as `.xai-cache/`) or accept hand-rolled fallback as the steady state.

**Resolution (2026-06-29):** Pre-downloaded binaries for `zizmor` and `actionlint` are now committed to `.audit-bin/`. The skill preflight adds `.audit-bin/` to `PATH` before attempting any network install, so sandbox runs no longer degrade. When upgrading scanner versions, update the binaries in `.audit-bin/` alongside the `ZIZMOR_VERSION` pin in the SKILL.md.
