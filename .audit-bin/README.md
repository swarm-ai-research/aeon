# .audit-bin/

Pre-cached scanner binaries for the `workflow-security-audit` skill. Committing them avoids
relying on PyPI or GitHub download scripts inside the Actions sandbox, where outbound
`bash <(curl …)` installers are blocked.

## Contents

| Binary | Version | Source |
|--------|---------|--------|
| `zizmor` | 1.25.2 | [zizmorcore/zizmor](https://github.com/zizmorcore/zizmor/releases) — Trail of Bits SARIF-capable GH Actions auditor |
| `actionlint` | 1.7.12 | [rhysd/actionlint](https://github.com/rhysd/actionlint/releases) — syntax-level workflow linter |
| `actionlint.tar.gz` | 1.7.12 | Archive the `actionlint` binary was extracted from (kept for provenance) |

## Updating a binary

1. Download the new release for `linux_amd64` from the upstream release page.
2. Replace the file in this directory and mark it executable (`chmod +x`).
3. Update the version row in the table above.
4. Update `ZIZMOR_VERSION` in `skills/workflow-security-audit/SKILL.md` step 0b to match.
5. Open a PR — do not commit directly to `main`.

## PATH wiring

The `workflow-security-audit` skill prepends `$PWD/.audit-bin` to `PATH` before checking
`command -v zizmor` / `command -v actionlint`, so these binaries are found first. The
`pipx` / `pip` / `curl` fallback paths in step 0b only activate when a binary is absent
(e.g. on a fresh checkout before this directory was added, or after a deliberate removal).
