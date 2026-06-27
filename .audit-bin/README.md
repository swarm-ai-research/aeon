# .audit-bin — pre-bundled scanner binaries

Pre-compiled binaries for `workflow-security-audit` committed here so the skill works inside the GitHub Actions Claude sandbox, which blocks `curl | bash` installers and `pipx`/`pip` network installs at runtime (see `memory/notes/sandbox-blocks-piped-curl-installers.md`).

## Contents

| File | Tool | Version | Platform |
|------|------|---------|----------|
| `actionlint` | [actionlint](https://github.com/rhysd/actionlint) — GitHub Actions workflow linter | v1.7.12 | linux/amd64 static |
| `actionlint.tar.gz` | actionlint release tarball (source of the binary above) | v1.7.12 | — |
| `zizmor` | [zizmor](https://github.com/zizmorcore/zizmor) — GitHub Actions static analyzer | 1.25.2 | linux/amd64 |

## How the skill uses these

`workflow-security-audit/SKILL.md` preflight (step 0b) checks for each tool on `$PATH` first, then falls back to this directory before attempting any network install:

```bash
export PATH="$REPO_ROOT/.audit-bin:$PATH"
```

## Updating

To bump a binary, download the new release from the upstream repo, replace the file here, and update the version table above and the `ZIZMOR_VERSION` / `ACTIONLINT_VERSION` constants in `workflow-security-audit/SKILL.md`.
