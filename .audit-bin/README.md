# .audit-bin — pre-cached security scanner binaries

Pre-built executables committed to the repo so `workflow-security-audit` can run
offline on GitHub Actions runners where outbound PyPI / curl installs may be blocked
by the sandbox.

## Contents

| File | Tool | Version | Committed |
|------|------|---------|-----------|
| `zizmor` | [zizmor](https://github.com/zizmorcore/zizmor) — Trail of Bits SARIF-capable GH Actions auditor | 1.25.2 | 2026-07-30 |
| `actionlint` | [actionlint](https://github.com/rhysd/actionlint) — syntax-level workflow linter | latest at commit time | 2026-07-30 |
| `actionlint.tar.gz` | Source archive for the `actionlint` binary above | — | 2026-07-30 |

## How the skill uses these

`skills/workflow-security-audit/SKILL.md` step 0b prepends `.audit-bin/` to `PATH`
when the executables are present, bypassing all network installs. Fall-back order:

1. `.audit-bin/<tool>` (this directory) — **primary on Actions runners**
2. System `PATH` / `~/.local/bin` (if already installed)
3. Network install (`pipx` / `curl-pipe`) — blocked in sandbox, degrades gracefully

## Updating the binaries

When `ZIZMOR_VERSION` in the SKILL.md is bumped:

1. Download the matching release from <https://github.com/zizmorcore/zizmor/releases>
   for the runner platform (currently `x86_64-unknown-linux-musl`).
2. Replace `.audit-bin/zizmor` and update this table's version and date.

For `actionlint`:

1. Download from <https://github.com/rhysd/actionlint/releases> (latest stable).
2. Replace `.audit-bin/actionlint` (and `actionlint.tar.gz` if kept) and update
   this table's date.

Commit both binaries together so the version record stays in sync.
