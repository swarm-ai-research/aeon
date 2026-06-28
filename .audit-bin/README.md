# .audit-bin — pre-fetched audit tool binaries

These binaries are checked into the repo so the `workflow-security-audit` skill can run inside the GitHub Actions sandbox, where outbound network calls from `bash` are blocked (no `curl`, no `pip install`, no `pipx`).

## Contents

| File | Tool | Version | Purpose |
|---|---|---|---|
| `zizmor` | [zizmor](https://docs.zizmor.sh) (Trail of Bits) | 1.25.2 | SARIF-capable semantic security scanner for GitHub Actions |
| `actionlint` | [actionlint](https://github.com/rhysd/actionlint) (Rhymond) | see binary | Syntax-level workflow linter with integrated shellcheck |
| `actionlint.tar.gz` | actionlint (compressed) | same | Tarball source for the `actionlint` binary above |

## Why these are committed

The `workflow-security-audit` skill normally installs scanners at runtime via `pipx install zizmor` and `bash <(curl …) actionlint`. Both paths fail inside the Aeon sandbox (observed 2026-06-21 — see `memory/notes/sandbox-blocks-piped-curl-installers.md`). The skill fell back to hand-rolled regex-only coverage and exited `WORKFLOW_AUDIT_TOOL_DEGRADED`.

Committing the binaries here follows the same prefetch pattern used by `.xai-cache/` and `scripts/prefetch-*.sh`: ship the tool alongside the skill rather than fetching it at runtime.

The skill's install step prepends `.audit-bin` to `PATH` before attempting any network installs, so the pre-fetched binaries are found first.

## Updating

To bump zizmor:
1. `pip download zizmor==<NEW_VERSION> --no-deps -d /tmp/zizmor-dl`
2. Extract the wheel, copy the binary to `.audit-bin/zizmor`
3. Update `ZIZMOR_VERSION` in `skills/workflow-security-audit/SKILL.md` step 0b
4. Remove and re-commit

To bump actionlint, download the release binary from the [actionlint releases page](https://github.com/rhysd/actionlint/releases), replace `.audit-bin/actionlint` and `.audit-bin/actionlint.tar.gz`, and commit.
