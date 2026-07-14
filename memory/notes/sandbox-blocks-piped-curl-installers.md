---
id: sandbox-blocks-piped-curl-installers
created: 2026-06-21
type: lesson
links: [[oauth-outage-zero-token-signature]]
---
# The Aeon sandbox blocks `bash <(curl …)` and direct exec of `~/.local/bin/*`, so audit skills that bootstrap their own scanner degrade to hand-rolled fallbacks

Observed on 2026-06-21 when `workflow-security-audit` tried to install/run `zizmor` and `actionlint`: both bootstrap paths failed inside the sandbox (the curl-pipe install is blocked, and pre-installed binaries under `~/.local/bin` aren't on PATH). The skill exited `WORKFLOW_AUDIT_TOOL_DEGRADED` with hand-rolled regex coverage only.

**Resolved:** binaries are now committed to `.audit-bin/` (added 2026-07-14). `workflow-security-audit` step 0b checks `.audit-bin/zizmor` and `.audit-bin/actionlint` before attempting any network install. This is the adopted pattern for audit-style skills — commit the binary directly rather than relying on a prefetch script or network install at runtime. When upgrading either tool, replace the binary in `.audit-bin/` and bump `ZIZMOR_VERSION` in the SKILL.md.
