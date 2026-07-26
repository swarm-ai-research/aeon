# .audit-bin — pre-built scanner binaries

Pre-compiled executables committed here so the `workflow-security-audit` skill can run
offline on GitHub Actions runners without hitting PyPI or curl-piped installers.

## Contents

| File | Tool | Version | Platform |
|------|------|---------|----------|
| `zizmor` | [zizmor](https://github.com/zizmorcore/zizmor) — SARIF-capable GH Actions auditor | 1.25.2 | linux/amd64 |
| `actionlint` | [actionlint](https://github.com/rhysd/actionlint) — workflow syntax/semantic linter | 1.7.12 | linux/amd64 |
| `actionlint.tar.gz` | actionlint source archive (kept as a fallback extraction target) | 1.7.12 | linux/amd64 |

## Upgrade instructions

**zizmor** — version is also pinned as `ZIZMOR_VERSION` in
`skills/workflow-security-audit/SKILL.md`. Bump both together:

```bash
pip install "zizmor==<new-version>"
cp "$(which zizmor)" .audit-bin/zizmor
```

**actionlint** — version is tracked in `ACTIONLINT_VERSION` in
`skills/workflow-security-audit/SKILL.md`. Bump both together:

```bash
bash <(curl -sL https://raw.githubusercontent.com/rhysd/actionlint/main/scripts/download-actionlint.bash) <new-version>
cp actionlint .audit-bin/actionlint
tar czf .audit-bin/actionlint.tar.gz actionlint
```

After replacing binaries, commit with `git add .audit-bin/` and update the version table above.
