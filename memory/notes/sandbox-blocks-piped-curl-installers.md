---
id: sandbox-blocks-piped-curl-installers
created: 2026-06-21
type: lesson
links: [[oauth-outage-zero-token-signature]]
---
# The Aeon sandbox blocks `bash <(curl …)` and direct exec of `~/.local/bin/*`, so audit skills that bootstrap their own scanner degrade to hand-rolled fallbacks

Observed on 2026-06-21 when `workflow-security-audit` tried to install/run `zizmor` and `actionlint`: both bootstrap paths failed inside the sandbox (the curl-pipe install is blocked, and pre-installed binaries under `~/.local/bin` aren't on PATH). The skill exited `WORKFLOW_AUDIT_TOOL_DEGRADED` with hand-rolled regex coverage only.

**Resolved (2026-07-02):** `zizmor` and `actionlint` binaries are now committed directly to `.audit-bin/` in the repo. The skill prepends `.audit-bin/` to `$PATH` in step 0b so the pre-shipped binaries are found before any network install is attempted. New audit-style skills should adopt the same pattern: commit the scanner binary to `.audit-bin/` and prepend `.audit-bin/` to `$PATH` in the install step.
