`VULN_SCANNER_OK · 0 code vulns · 1 dep-bump drafted · 23 OSV advisories bundled`

## Summary

Ran `skills/vuln-scanner/SKILL.md` against **LosaLosSantos/aurelio-finance** (1,894★, Python+TypeScript wealth-management desktop app) at HEAD `d3c1068`. Weekly cadence on time (prev run 2026-10-03 against KKKKhazix/AIHOT).

**Scanners:** semgrep=ok, trufflehog(fs+git)=ok, osv=ok, slither=n/a. Used direct `git clone --depth=200` per [[github-app-cannot-fork-third-party-repos]].

**Findings:**
- **0 confirmed code vulnerabilities.** 4 semgrep WARNINGs were all `github-actions-mutable-action-tag` on a secrets-free CI workflow — triaged out. App is tightly scoped: localhost-only uvicorn, CORS pinned to `:5173`, MCP server stdio+SQLite-ro, no subprocess/eval/pickle/yaml.load across backend.
- **0 verified secrets** (fs + full git history).
- **23 public OSV advisories across 6 transitive PyPI pkgs** in `backend/uv.lock`: 1 CRIT (anyio IDNA 2003 TLS spoof), 2 HIGH (starlette form-DoS, urllib3 chunk-size), 19 MODERATE, 1 LOW. Fix is lockfile-only: `cd backend && uv lock --upgrade-package anyio …` across the six.

**Channel:** 1 public-pr dep-bump drafted to `.pending-disclosure/LosaLosSantos-aurelio-finance-2026-10-10T170000Z-deps.md` for operator out-of-band submission. 0 PVR drafted (no exploitable code vulns + repo has no SECURITY.md / unreadable PVR status).

**Files created/modified:**
- `.pending-disclosure/LosaLosSantos-aurelio-finance-2026-10-10T170000Z-deps.md`
- `articles/vuln-scan-2026-10-10.md`
- `memory/vuln-scanned.json` (run #17 appended)
- `.pending-notify/1791651647-vuln-scanner.md`
- `memory/logs/2026-10-10.md` (vuln-scanner entry + summary)

**Follow-ups:** operator submits the dep-bump PR out-of-band. Standing action-queue item to land the `git clone`-instead-of-`gh repo fork` SKILL.md edit is still owed (worked around in-flight today).
