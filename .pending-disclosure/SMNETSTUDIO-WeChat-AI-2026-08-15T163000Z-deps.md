# Public Dependency-Bump PR — SMNETSTUDIO/WeChat-AI

**Repo:** https://github.com/SMNETSTUDIO/WeChat-AI
**HEAD scanned:** `1f56c7f77623d0223164fb3ce97b0f2e48f6ca6f`
**Scanned by:** Aeon (osv-scanner)
**Drafted:** 2026-08-15T16:30:00Z — hold for operator submission
**Channel:** Public PR (all CVEs below are already disclosed via GHSA)

## Sandbox note
Aeon's GitHub App cannot fork third-party repos (per [[github-app-cannot-fork-third-party-repos]]; HTTP 403 on `POST /repos/{owner}/{repo}/forks`), so this PR must be filed by the operator from a personal fork. All content below is ready-to-paste.

## Fork + branch (operator)
```bash
gh repo fork SMNETSTUDIO/WeChat-AI --clone --default-branch-only
cd WeChat-AI
git checkout -b security/bump-vulnerable-deps-2026-08-15
# ... apply changes below ...
git commit -m "fix(deps): bump vulnerable transitives (starlette, fast-uri, find-my-way, idna, pytest)"
git push -u origin HEAD
gh pr create --repo SMNETSTUDIO/WeChat-AI --title "..." --body "$(cat body.md)"
```

## PR title
```
fix(deps): bump vulnerable transitives — starlette, fast-uri, find-my-way, idna, pytest
```

## PR body

Automated dependency bump for six packages carrying disclosed CVEs. All are transitive dependencies of currently-pinned direct deps; the fix is either a direct-dep bump that pulls the fixed transitive, or a lockfile update via `pnpm dedupe` / `pip-compile`.

### JS / pnpm-lock.yaml (transitive of `fastify@5.2.1`)

| Package | Current | Fixed | CVEs | Severity |
|---|---|---|---|---|
| `fast-uri` (2 copies: 3.1.3 + 4.1.0) | 3.1.3, 4.1.0 | 3.1.5, 4.1.2 | GHSA-7p8r-x3mc-p8w7, GHSA-v2hh-gcrm-f6hx | High (integrity — host confusion via backslash authority delimiter) |
| `find-my-way` | 9.6.0 | 9.7.0 | GHSA-c96f-x56v-gq3h | High (availability — HTTP/2 DoS) |

**Fix:** `pnpm update fastify @fastify/compress --latest && pnpm dedupe` in the repo root should update fastify's transitive tree. If dedupe leaves both `fast-uri` majors in place (common with peer-dep constraints), pin via `pnpm.overrides` in the root `package.json`:

```json
"pnpm": {
  "overrides": {
    "fast-uri@3": "3.1.5",
    "fast-uri@4": "4.1.2",
    "find-my-way": "9.7.0"
  }
}
```

Then re-run `pnpm install` and commit the resulting `pnpm-lock.yaml` diff.

### Python / huggingface/wechat-ai-tools/requirements.txt

| Package | Current | Fixed | CVEs | Severity |
|---|---|---|---|---|
| `starlette` (transitive via `fastapi==0.115.12`) | 0.46.2 | 1.3.1 | 14 CVEs (GHSA-2c2j-9gv5-cj73, -7f5h-v6xp-fcq8, -82w8-qh3p-5jfq, -86qp-5c8j-p5mr, -jp82-jpqv-5vv3, -wqp7-x3pw-xc5r, -x746-7m8f-x49c; PYSEC-2026-161, -1941, -1942, -2280, -2281, -248, -249) | Mixed — DoS, host-header poisoning, arbitrary HTTP dispatch to HTTPEndpoint attrs |
| `idna` (transitive via `httpx==0.28.1`) | 3.9.0 | 3.15 | GHSA-65pc-fj4g-8rjx, PYSEC-2026-215 | Low (DoS via crafted encode input) |
| `pytest` (dev) | 8.3.5 | 9.0.3 | GHSA-6w46-j5rx-g56g, PYSEC-2026-1845 | Low (vulnerable tmpdir handling — dev only) |

**Fix (starlette + idna):** the direct pins `fastapi==0.115.12` and `httpx==0.28.1` pull the vulnerable transitives. Two options:
- **Option A (recommended):** bump the parents to versions that pull fixed transitives — `fastapi>=0.118` (pulls `starlette>=1.3.1`), `httpx>=0.29` (pulls `idna>=3.15`). Verify HF Space still boots (`uvicorn app:app --port 7860`).
- **Option B (minimal delta):** pin the transitives directly in `requirements.txt`:
  ```
  starlette>=1.3.1
  idna>=3.15
  ```

**Fix (pytest):** dev-only, no runtime impact. Bump `pytest==8.3.5` → `pytest==9.0.3` and re-run the test suite. If breakage, consider deferring.

### Verification
- `pnpm install --frozen-lockfile` succeeds after lockfile updates.
- `pnpm --filter @wechat-ai/api typecheck && pnpm --filter @wechat-ai/api test` still passes.
- `pip install -r huggingface/wechat-ai-tools/requirements.txt` succeeds.
- `pytest huggingface/wechat-ai-tools/tests` still passes.

### References
- osv-scanner report source: https://google.github.io/osv-scanner/
- All GHSAs viewable at https://github.com/advisories/{GHSA-ID}
- No code changes outside lockfile / requirements.txt (+ optional overrides block in root package.json).

---
Filed by [Aeon](https://github.com/aeonframework/aeon).
