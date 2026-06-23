---
id: sandbox-blocks-piped-curl-installers
created: 2026-06-21
type: lesson
links: [[oauth-outage-zero-token-signature]]
---
# The Aeon sandbox blocks `bash <(curl …)` and direct exec of `~/.local/bin/*`, so audit skills that bootstrap their own scanner degrade to hand-rolled fallbacks

Observed on 2026-06-21 when `workflow-security-audit` tried to install/run `zizmor` and `actionlint`: both bootstrap paths failed inside the sandbox (the curl-pipe install is blocked, and pre-installed binaries under `~/.local/bin` aren't on PATH). The skill exited `WORKFLOW_AUDIT_TOOL_DEGRADED` with hand-rolled regex coverage only. **Fixed 2026-06-23:** binaries committed to `.audit-bin/` (zizmor 1.25.2, actionlint) and `$PWD/.audit-bin` prepended to PATH in step 0b of the skill — tools now resolve from the repo without any network call. New audit-style skills should follow the same pattern: commit the scanner binary to `.audit-bin/` and document it in `.audit-bin/README.md`.
