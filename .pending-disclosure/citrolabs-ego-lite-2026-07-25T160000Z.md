---
repo: citrolabs/ego-lite
scanned_at: 2026-07-25T16:00:00Z
head_sha: 02ee972edf0685371c826c90421511f8a2940cd5
channel: pvr
pvr_endpoint: POST /repos/citrolabs/ego-lite/security-advisories
severity: medium
cwe_ids: ["CWE-78", "CWE-77"]
detected_by: [semgrep]
status: drafted — pending operator submission
notes: repo has no SECURITY.md; PVR endpoint reachable (returns empty advisories list). Do NOT submit publicly (issue/PR) — file only via PVR or private contact.
---

## Draft PVR body

**Title:** GitHub Actions shell injection via unquoted `github.head_ref` in `main-pr-source.yml`

### Summary
The workflow `.github/workflows/main-pr-source.yml` interpolates `${{ github.head_ref }}` directly inside a `run:` step. On `pull_request` events, `github.head_ref` is the source branch name, which is fully controllable by anyone opening a pull request from a fork. Because it is expanded before the shell parses the surrounding script, a branch name containing shell metacharacters can execute arbitrary commands on the workflow runner.

### Impact
Any unauthenticated user who forks `citrolabs/ego-lite` and opens a pull request against `main` with a specially-crafted branch name can execute arbitrary shell commands on the GitHub-hosted runner. The workflow trigger is `pull_request` (not `pull_request_target`), so `GITHUB_TOKEN` is scoped read-only and repository secrets are not exposed to fork PRs — but the attacker still gains:
- Arbitrary shell execution in the workflow runner sandbox
- Access to the read-only `GITHUB_TOKEN` (can enumerate repo metadata, download artifacts across the workflow's job graph)
- A foothold to fetch second-stage payloads and pivot via GitHub Actions primitives (artifacts, environment files, `GITHUB_ENV`, `GITHUB_OUTPUT`, `GITHUB_PATH`)

Severity: **medium** (arbitrary code execution scoped to a read-only-token runner; escalates to **high** if this workflow is ever changed to `pull_request_target` or has its `permissions:` widened).

### Location
`.github/workflows/main-pr-source.yml:14` (repo HEAD `02ee972edf0685371c826c90421511f8a2940cd5`)

```yaml
      - name: Require dev branch
        run: |
          if [ "${{ github.head_ref }}" != "dev" ]; then
            echo "Pull requests into main must come from the dev branch."
            exit 1
          fi
```

### Proof of exploitation (concept, no working chain)
Git permits `;`, `$`, `"`, and backticks inside branch names. A PR opened from a fork with a branch named (for example) `dev";id;#` yields a rendered step body of:

```bash
if [ "dev";id;#" != "dev" ]; then
```

which executes `id` and returns. No working exploit chain is included; the primitive is a standard GitHub Actions `run:` step injection documented by GitHub's own security guidance and by Semgrep rule `yaml.github-actions.security.run-shell-injection.run-shell-injection` (ERROR severity).

### Suggested fix
Route the untrusted value through an intermediate environment variable so it is never interpolated into the shell body:

```yaml
      - name: Require dev branch
        env:
          HEAD_REF: ${{ github.head_ref }}
        run: |
          if [ "$HEAD_REF" != "dev" ]; then
            echo "Pull requests into main must come from the dev branch."
            exit 1
          fi
```

The same pattern (env-var indirection for any `${{ github.* }}` value that is not a fixed enum or a validated SHA) should be applied to any future `run:` step that references PR-author-controlled context.

### Related low-signal findings (not filed)
Semgrep additionally flagged 12 `github-actions-mutable-action-tag` warnings against unpinned `actions/checkout@v4`, `actions/setup-node@v4`, `actions/upload-artifact@v4`, and `actions/download-artifact@v4` references across `ci.yml`, `quality-gates.yml`, and `publish-ego-browser-skill.yml`. These are supply-chain hygiene, not a live vulnerability, and are typically addressed by Dependabot rather than an outside report; not filed. `github.event_name`, `github.event.pull_request.base.sha`, and `github.event.before` interpolations in the same workflows are enum-typed or SHA-typed and not exploitable.

### Detected by
Aeon vuln-scanner + semgrep `p/security-audit` (rule `yaml.github-actions.security.run-shell-injection.run-shell-injection`)

---

## Suggested PVR POST payload

```bash
gh api -X POST "/repos/citrolabs/ego-lite/security-advisories" \
  -H "X-GitHub-Api-Version: 2026-03-10" \
  -f summary="GitHub Actions shell injection via unquoted github.head_ref in main-pr-source.yml" \
  -f description="$(cat body.md)" \
  -f severity="medium" \
  -F cwe_ids='["CWE-78","CWE-77"]'
```

If the endpoint returns 404/403, PVR is disabled. Fall back to `SECURITY.md` (currently absent) or a private contact on the maintainer's org profile. Do **not** open a public issue or PR — the primitive is unpatched and public disclosure creates a zero-day for any fork of ego-lite.
