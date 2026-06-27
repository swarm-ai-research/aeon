# .audit-bin — pre-seeded scanner binaries

Pre-committed binaries for the `workflow-security-audit` skill.

The GitHub Actions sandbox blocks `bash <(curl …)` installer pipes and does not
carry `~/.local/bin` on PATH, so `zizmor` and `actionlint` cannot be installed at
runtime via `pipx` / `pip` / the actionlint download script. This directory works
around that by committing the binaries directly; the skill checks here first before
attempting a live install.

## Contents

| File | Tool | Version committed |
|---|---|---|
| `zizmor` | [zizmor](https://github.com/zizmorcore/zizmor) — Trail of Bits GH Actions SARIF auditor | 1.25.2 |
| `actionlint` | [actionlint](https://github.com/rhysd/actionlint) — workflow syntax/security linter | (see binary) |
| `actionlint.tar.gz` | upstream release tarball for provenance | — |

## Update procedure

When bumping tool versions, replace the binary in-place and update the version
note in `skills/workflow-security-audit/SKILL.md` (`ZIZMOR_VERSION` constant and
the `## Contents` table above).

## Why committed, not gitignored

`.audit-tmp/` and `.audit*.py` are ignored (scratch/debug artifacts). This
directory intentionally stays tracked — it is the durable binary cache, not a
per-run scratch directory.
