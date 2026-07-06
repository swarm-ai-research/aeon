---
id: sandbox-blocks-piped-curl-installers
created: 2026-06-21
type: lesson
links: [[oauth-outage-zero-token-signature]]
---
# The Aeon sandbox blocks `bash <(curl …)` and direct exec of `~/.local/bin/*`, so audit skills that bootstrap their own scanner degrade to hand-rolled fallbacks

Observed on 2026-06-21 when `workflow-security-audit` tried to install/run `zizmor` and `actionlint`: both bootstrap paths failed inside the sandbox (the curl-pipe install is blocked, and pre-installed binaries under `~/.local/bin` aren't on PATH). The skill exited `WORKFLOW_AUDIT_TOOL_DEGRADED` with hand-rolled regex coverage only. New audit-style skills should either ship the scanner via a prefetch script run before Claude (same pattern as `.xai-cache/`), commit scanner binaries under `.audit-bin/` and export `PATH="$PWD/.audit-bin:$PATH"` as the first step, or accept hand-rolled fallback as the steady state. As of 2026-07-06, `workflow-security-audit` uses the committed-binary approach: `.audit-bin/actionlint` and `.audit-bin/zizmor` are present in the repo and picked up automatically via the PATH export in step 0b.
