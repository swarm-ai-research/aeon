---
id: sandbox-blocks-piped-curl-installers
created: 2026-06-21
type: lesson
links: [[oauth-outage-zero-token-signature]]
---
# The Aeon sandbox blocks `bash <(curl …)` and direct exec of `~/.local/bin/*`, so audit skills that bootstrap their own scanner degrade to hand-rolled fallbacks

Observed on 2026-06-21 when `workflow-security-audit` tried to install/run `zizmor` and `actionlint`: both bootstrap paths failed inside the sandbox (the curl-pipe install is blocked, and pre-installed binaries under `~/.local/bin` aren't on PATH). The skill exited `WORKFLOW_AUDIT_TOOL_DEGRADED` with hand-rolled regex coverage only.

**Resolution (2026-06-30):** Pre-bundled `actionlint` and `zizmor` binaries were committed to `.audit-bin/`. Step 0b in the skill now prepends `.audit-bin/` to PATH before attempting any network install, so the tools resolve immediately inside the sandbox without network access. New audit-style skills should use the same pattern: commit the scanner binary to a `.XXX-bin/` directory and add that directory to PATH as the first install step.
