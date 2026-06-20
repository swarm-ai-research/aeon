---
target: omnigent-ai/omnigent
detected_at: 2026-06-20T06:00:00Z
channel: public-pr
reason_pending: Aeon's workflow token cannot fork external repos (HTTP 403 on POST /forks); the operator must open this PR manually from a fork they own.
draft_branch: security/bump-deps-2026-06
---

# Draft: `fix(deps): bump vulnerable dependencies in production lockfiles`

## Operator instructions

1. Fork `omnigent-ai/omnigent` to your own account: `gh repo fork omnigent-ai/omnigent --clone`.
2. Apply the bumps in the table below (run the install commands per ecosystem).
3. Commit on a `security/bump-deps-2026-06` branch.
4. Open the PR upstream with the body from `## PR body` below.

All advisories below are already publicly disclosed in OSV — opening a public PR with these bumps is the recommended channel (no zero-day risk).

## Findings (production lockfiles only)

| Lockfile | Package | Current | Fixed-in | Advisories | Highest CVSS |
|---|---|---|---|---|---|
| `uv.lock` | `cryptography` | 48.0.0 | 48.0.1 | GHSA-537c-gmf6-5ccf | 7.5 (DoS via vulnerable OpenSSL) |
| `uv.lock` | `pydantic-settings` | 2.14.1 | 2.14.2 | GHSA-4xgf-cpjx-pc3j | 5.3 (symlink escape in `NestedSecretsSettingsSource`) |
| `uv.lock` | `starlette` | 0.52.1 | **see note** | PYSEC-2026-161, GHSA-82w8-qh3p-5jfq, GHSA-86qp-5c8j-p5mr, GHSA-jp82-jpqv-5vv3, GHSA-wqp7-x3pw-xc5r, GHSA-x746-7m8f-x49c | 7.5 (SSRF + NTLM theft via UNC in StaticFiles on Windows) |
| `ap-web/package-lock.json` | `dompurify` | 3.4.10 | 3.4.11 | GHSA-cmwh-pvxp-8882 | 5.1 (permanent `ALLOWED_ATTR` pollution via `setConfig()`) |
| `ap-web/package-lock.json` | `undici` | 7.27.2 | 7.28.0 | GHSA-35p6-xmwp-9g52, GHSA-g8m3-5g58-fq7m, GHSA-hm92-r4w5-c3mj, GHSA-p88m-4jfj-68fv, GHSA-pr7r-676h-xcf6, GHSA-vmh5-mc38-953g, GHSA-vxpw-j846-p89q | 8.8 (cross-origin routing via SOCKS5 proxy pool reuse) |
| `ap-web/electron/package-lock.json` | `form-data` | 4.0.5 | 4.0.6 | GHSA-hmw2-7cc7-3qxx | 8.7 (CRLF injection via unescaped multipart field names) |
| `ap-web/electron/package-lock.json` | `undici` | 6.26.0 | 6.27.0 | GHSA-35p6-xmwp-9g52, GHSA-g8m3-5g58-fq7m, GHSA-p88m-4jfj-68fv, GHSA-vxpw-j846-p89q | 7.5 (HTTP header injection via Set-Cookie percent-decoding) |
| `ap-web/electron/package-lock.json` | `undici` | 7.27.2 | 7.28.0 | (same 7 advisories as ap-web above) | 8.8 |

### Starlette note

`starlette` 0.52.1 has fixes published only on the `1.x` line (`1.0.1`, `1.1.0`, `1.3.0`, `1.3.1`). This is a **major-version bump** and may interact with the project's FastAPI/Starlette pinning constraints — please verify the chosen upgrade path against your `pyproject.toml`'s declared range before merging. If FastAPI itself isn't compatible with `starlette>=1`, consider backporting the patches or temporarily disabling the affected surfaces (StaticFiles, request.url.path/hostname-derived auth checks) until upstream rolls forward.

The six advisories center on host/path-header validation gaps in Starlette's request abstraction — if the application uses `request.url.path` for any auth or routing decision, the risk is real and not theoretical.

### Out of scope (intentionally excluded)

- `tests/codex_parity/sidecar/Cargo.lock` — 11 RUSTSEC/GHSA hits across `gix*`, `hickory-proto`, `jsonwebtoken`, `tar`, `paste`, etc. **Test-only** dependency tree (codex-parity sidecar). Not shipped to users; skill rule "drop findings in `test/` paths" applies.

## Suggested commands (run from your fork)

```bash
# Python deps (uv)
uv lock --upgrade-package cryptography --upgrade-package pydantic-settings
# starlette: edit pyproject.toml to the chosen 1.x bound, then:
uv lock --upgrade-package starlette

# Web frontend
( cd ap-web && npm install dompurify@^3.4.11 undici@^7.28.0 && npm dedupe )

# Electron desktop
( cd ap-web/electron && npm install form-data@^4.0.6 undici@^7.28.0 && npm dedupe )
# undici 6.x is also present transitively; npm dedupe + an explicit override
# may be required to lift it to 6.27.0+:
#   "overrides": { "undici@6": "^6.27.0" }
```

## PR body

> ### Summary
>
> Bumps a set of production dependencies to address disclosed CVEs flagged by [osv-scanner](https://google.github.io/osv-scanner/) against the current lockfiles. All advisories are already public; no embargoed information is included.
>
> ### Packages bumped
>
> | Ecosystem | Package | Before → After | Advisories |
> |---|---|---|---|
> | PyPI | `cryptography` | 48.0.0 → 48.0.1 | [GHSA-537c-gmf6-5ccf](https://github.com/advisories/GHSA-537c-gmf6-5ccf) |
> | PyPI | `pydantic-settings` | 2.14.1 → 2.14.2 | [GHSA-4xgf-cpjx-pc3j](https://github.com/advisories/GHSA-4xgf-cpjx-pc3j) |
> | PyPI | `starlette` | 0.52.1 → (1.x — see PR description) | 6 advisories incl. [GHSA-wqp7-x3pw-xc5r](https://github.com/advisories/GHSA-wqp7-x3pw-xc5r) (SSRF) |
> | npm | `dompurify` (ap-web) | 3.4.10 → 3.4.11 | [GHSA-cmwh-pvxp-8882](https://github.com/advisories/GHSA-cmwh-pvxp-8882) |
> | npm | `undici` (ap-web, electron) | 7.27.2 → 7.28.0 | 7 advisories incl. [GHSA-hm92-r4w5-c3mj](https://github.com/advisories/GHSA-hm92-r4w5-c3mj) (SOCKS5 cross-origin) |
> | npm | `undici` (electron, 6.x) | 6.26.0 → 6.27.0 | 4 advisories |
> | npm | `form-data` (electron) | 4.0.5 → 4.0.6 | [GHSA-hmw2-7cc7-3qxx](https://github.com/advisories/GHSA-hmw2-7cc7-3qxx) (CRLF injection) |
>
> ### Notes
>
> - The starlette upgrade crosses the 1.0 boundary; verify against any FastAPI constraint before merging.
> - Cargo-side RUSTSEC findings in `tests/codex_parity/sidecar/` are not addressed here; they live in a test-only dependency tree.
> - No SAST findings of concern were observed in the audit: semgrep raised 47 candidates across `security-audit`, `owasp-top-ten`, and `secrets` rulesets, all of which triaged to false positives or by-design trusted-input call sites after manual review. trufflehog (`--only-verified`) returned zero secrets across the filesystem and the full git history.
>
> ---
> Findings collected by [Aeon](https://github.com/aeonframework/aeon)'s `vuln-scanner` skill on 2026-06-20.
