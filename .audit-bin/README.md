# .audit-bin/

Pre-cached scanner binaries committed so `workflow-security-audit` can run on GitHub Actions runners without hitting sandbox-blocked network installs (`bash <(curl …)` and PyPI are blocked in the Aeon sandbox).

## Contents

| File | Tool | Version |
|------|------|---------|
| `zizmor` | [zizmor](https://github.com/woodruffw/zizmor) — SARIF-capable GH Actions auditor (Trail of Bits) | 1.25.2 (matches `ZIZMOR_VERSION` in SKILL.md) |
| `actionlint` | [actionlint](https://github.com/rhysd/actionlint) — syntax-level workflow linter | run `./actionlint --version` to check |
| `actionlint.tar.gz` | Source archive for `actionlint` (kept for re-extraction if needed) | — |

Binaries are linux/amd64 musl-linked so they run on any GitHub-hosted ubuntu runner without extra dependencies.

## How to update

1. Download the new release binary for the runner platform (linux/amd64):
   - zizmor: `gh release download vX.Y.Z -R woodruffw/zizmor -p 'zizmor-x86_64-unknown-linux-musl.tar.gz'`
   - actionlint: `gh release download vX.Y.Z -R rhysd/actionlint -p 'actionlint_X.Y.Z_linux_amd64.tar.gz'`
2. Extract, `chmod +x`, and replace the binary here.
3. Bump `ZIZMOR_VERSION` in `skills/workflow-security-audit/SKILL.md` (zizmor only — actionlint version is not yet pinned there).
4. Commit the updated binary and the SKILL.md version bump together.
