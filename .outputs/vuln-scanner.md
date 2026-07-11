All tasks complete. Clean git status: `.gitignore`, `memory/logs/2026-07-11.md`, `memory/vuln-scanned.json`, `articles/vuln-scan-2026-07-11.md`, `.pending-disclosure/` staged, and `.pending-notify/1783789481-vuln-scanner.md` written (gitignored — will fan out via the workflow's post-process step).

## Summary

**Target:** `oomol-lab/open-connector` (1,349★, TypeScript OAuth-credential-broker gateway, Apache-2.0), scanned at HEAD `62796b0d…`.

**Scanner status:** `semgrep=ok · trufflehog-fs=ok · trufflehog-git=ok · osv=ok · slither=n/a`. 13 semgrep candidates → **1 confirmed** in-scope finding.

**Confirmed finding — routed to PVR:** `src/server/secrets/secret-codec.ts:48` — AES-256-GCM `createDecipheriv` called without `authTagLength` and `setAuthTag` accepts any NIST-permitted tag length. An attacker with credential-store write access reduces forgery cost from ~2^-128 to ~2^-32 by supplying a 4-byte tag. The Cloudflare Worker sibling codec is unaffected (WebCrypto default tagLength=128). Fix is three lines. Matches SECURITY.md's first-in-scope call-out: "Credential storage and at-rest encryption (`src/server/secrets/*`)."

**Dropped:** Dockerfile-runs-as-root and 11× GHA-mutable-action-tag warnings — both out of scope per the maintainer's stated SECURITY.md.

**Dependency posture:** 0 vulnerabilities across 669 packages. No public dep-CVE PR to draft. TruffleHog verified 0 secrets across 32 MB of filesystem + git history.

**Channels:** GHA token could not create the advisory (HTTP 403 `Resource not accessible by integration`, same class as `[[github-actions-cannot-create-prs]]`) nor fork the repo. PVR draft staged for operator submission via the maintainer's preferred URL or `support@oomol.com`. No public PR opened — correct per skill rules.

**Files:**
- `articles/vuln-scan-2026-07-11.md` — local report (exploit specifics redacted)
- `.pending-disclosure/oomol-lab-open-connector-2026-07-11T170000Z.md` — full PVR draft (threat model, non-forgery PoC, 3-line fix)
- `memory/vuln-scanned.json` — appended (30-day dedup)
- `memory/logs/2026-07-11.md` — appended `## vuln-scanner` entry
- `.pending-notify/1783789481-vuln-scanner.md` — notification queued
- `.gitignore` — added `.scratch/` to prevent scanner temp files being committed

**Follow-up:** operator submits the PVR draft through the private channel; the fix is small enough to be cherry-picked directly by the maintainer, so no fork-based patch branch is required.
