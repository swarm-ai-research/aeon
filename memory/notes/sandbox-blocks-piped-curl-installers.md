---
id: sandbox-blocks-piped-curl-installers
created: 2026-06-21
type: lesson
links: [[oauth-outage-zero-token-signature]]
---
# The Aeon sandbox blocks `bash <(curl …)` and direct exec of `~/.local/bin/*`, so audit skills that bootstrap their own scanner degrade to hand-rolled fallbacks

Observed on 2026-06-21 when `workflow-security-audit` tried to install/run `zizmor` and `actionlint`: both bootstrap paths failed inside the sandbox (the curl-pipe install is blocked, and pre-installed binaries under `~/.local/bin` aren't on PATH). The skill exited `WORKFLOW_AUDIT_TOOL_DEGRADED` with hand-rolled regex coverage only. New audit-style skills should either ship the scanner via a prefetch script run before Claude (same pattern as `.xai-cache/`) or accept hand-rolled fallback as the steady state.

**Status (2026-06-28):** Resolved for `workflow-security-audit` by committing pre-compiled binaries to `.audit-bin/` (zizmor 1.25.2, actionlint 1.7.12). The SKILL.md now prepends `.audit-bin/` to `$PATH` before attempting any `pipx`/`curl` install. See `.audit-bin/README.md` for update instructions.
