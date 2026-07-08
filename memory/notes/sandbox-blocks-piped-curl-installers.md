---
id: sandbox-blocks-piped-curl-installers
created: 2026-06-21
type: lesson
links: [[oauth-outage-zero-token-signature]]
---
# The Aeon sandbox blocks `bash <(curl …)` and direct exec of `~/.local/bin/*`, so audit skills that bootstrap their own scanner degrade to hand-rolled fallbacks

Observed on 2026-06-21 when `workflow-security-audit` tried to install/run `zizmor` and `actionlint`: both bootstrap paths failed inside the sandbox (the curl-pipe install is blocked, and pre-installed binaries under `~/.local/bin` aren't on PATH). The skill exited `WORKFLOW_AUDIT_TOOL_DEGRADED` with hand-rolled regex coverage only.

**Resolution (applied after 2026-06-21):** pre-shipped x86-64 Linux binaries for both tools committed to `.audit-bin/` in the repo root. `workflow-security-audit` now exports `PATH="$(pwd)/.audit-bin:$HOME/.local/bin:$PATH"` at the top of step 0b, so the binaries resolve without any network call. New audit-style skills should use the same pattern — commit static binaries to `.audit-bin/` and prepend it to PATH before attempting pip/curl installs.
