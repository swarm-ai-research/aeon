---
id: sandbox-blocks-piped-curl-installers
created: 2026-06-21
type: lesson
links: [[oauth-outage-zero-token-signature]]
---
# The Aeon sandbox blocks `bash <(curl …)` and direct exec of `~/.local/bin/*`, so audit skills that bootstrap their own scanner degrade to hand-rolled fallbacks

Observed on 2026-06-21 when `workflow-security-audit` tried to install/run `zizmor` and `actionlint`: both bootstrap paths failed inside the sandbox (the curl-pipe install is blocked, and pre-installed binaries under `~/.local/bin` aren't on PATH). The skill exited `WORKFLOW_AUDIT_TOOL_DEGRADED` with hand-rolled regex coverage only.

**Resolution (implemented ~2026-06-28):** committed pre-downloaded linux_amd64 release binaries to `.audit-bin/zizmor` and `.audit-bin/actionlint`. Step 0b of the skill now checks `[ -x ".audit-bin/zizmor" ]` before attempting any network install, so the full SARIF scan runs without a network round-trip. This is the recommended pattern for audit-style skills that need scanner binaries: commit binaries to `.audit-bin/`, fall back to prefetch script or inline install only when absent.

New audit-style skills should use the same `.audit-bin/` approach rather than relying on `pipx`/`curl` at runtime.
