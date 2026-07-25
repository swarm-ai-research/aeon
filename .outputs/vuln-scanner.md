All artifacts in place. `.vuln-scan/` is gitignored so the scanner JSON blobs won't be committed.

## Summary

Ran the Saturday 07-25 16:00Z **vuln-scanner** slot against **citrolabs/ego-lite** (~3.3k stars, JS/TS, trending +986 today, "share logged-in browser state with AI agents" — credential-adjacent surface, first-time scan).

**Scanner status:** semgrep=ok (13 hits), trufflehog=ok (0 verified secrets in fs + git history), osv=ok (0 vulnerable deps across 87 packages), slither=n/a. Fork step blocked (HTTP 403, aeon-bot token per [[github-actions-cannot-create-prs]]) → direct clone fallback at HEAD `02ee972`.

**Triage:** 13 candidates → **1 confirmed medium** — GitHub Actions shell injection via unquoted `${{ github.head_ref }}` in `.github/workflows/main-pr-source.yml`. Any fork PR author can execute shell on the runner via a specially-crafted branch name. Trigger is `pull_request` (read-only token, no secrets), so scope is RCE-on-runner without secret exfiltration; escalates to high if the workflow ever moves to `pull_request_target`. 12 mutable-action-tag warnings dropped as supply-chain hygiene, not a live vuln.

**Disclosure:** PVR drafted to `.pending-disclosure/citrolabs-ego-lite-2026-07-25T160000Z.md` (repo has no SECURITY.md; PVR endpoint reachable). No auto-submit — operator applies the `gh api -X POST /repos/citrolabs/ego-lite/security-advisories` payload out of band per established pattern. Do **not** open a public issue/PR — primitive is unpatched.

**Files:** `articles/vuln-scan-2026-07-25.md` (new, file/line redacted), `.pending-disclosure/citrolabs-ego-lite-2026-07-25T160000Z.md` (new, full detail + suggested fix), `memory/vuln-scanned.json` (+1 entry, 7th total), `.pending-notify/1784997881-vuln-scanner.md` (new), `memory/logs/2026-07-25.md` (`## Vuln Scanner` section appended). `.pending-disclosure/` queue depth now 2 (this + `oomol-lab/open-connector` 14d).

**Follow-up:** operator to submit PVR; MEMORY.md `.pending-disclosure/` line to move `1 entry` → `2 entries` on next flush.
