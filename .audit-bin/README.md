# .audit-bin — pre-bundled scanner binaries

Pre-compiled static analysis binaries committed directly to the repo so the
`workflow-security-audit` skill can use them even when the GitHub Actions
sandbox blocks outbound pip/curl installs at runtime.

## Binaries

| Binary | Tool | Version | Source |
|--------|------|---------|--------|
| `actionlint` | [rhysd/actionlint](https://github.com/rhysd/actionlint) — workflow syntax linter | see release tag in tarball | downloaded via `scripts/download-actionlint.bash` |
| `actionlint.tar.gz` | same — original archive kept for provenance | | |
| `zizmor` | [zizmorcore/zizmor](https://github.com/zizmorcore/zizmor) — SARIF-capable GHA security auditor | v1.25.2 | `pip install zizmor==1.25.2` |

## Why these exist

The `workflow-security-audit` skill tries to `pip install zizmor` and `curl |
bash` actionlint at runtime. Both can be blocked by the GHA sandbox (see
CLAUDE.md §Sandbox Limitations). Committing the binaries here lets the skill
add `.audit-bin/` to `$PATH` as a first-pass fallback before attempting live
installs.

## How to update

1. Download the new release binary (Linux x86-64).
2. Replace the file in `.audit-bin/`.
3. Bump `ZIZMOR_VERSION` in `skills/workflow-security-audit/SKILL.md` to match.
4. Commit on a branch and open a PR — do not commit directly to `main`.
