## Summary

Executed `skills/vuln-scanner/SKILL.md` end-to-end against **`unstablebuild/rune`** (985★, Go, "the development environment for pros", `SECURITY.md` invites PVR + `security@unstable.build`). HEAD `2fc4d8251` at 2026-09-19T15:06Z+02:00.

**Scanner status:** semgrep=ok (83 candidates) · trufflehog=ok (0 verified, 0 unverified across 160 MB fs + 68 MB git history) · osv-scanner=ok (10 advisories across 6 production packages) · slither=n/a (no `*.sol`).

**Confirmed findings (2):**
1. **PVR (medium, CWE-22/59/409)** — `internal/ide/idepkg/manager.go:1854-1913` `untar` skips zip-slip guard, does not sanitise `os.Symlink(hdr.Linkname, target)`, and copies unbounded via `io.Copy`. `gitpkg`-typed installs skip `Manager.trust.VerifyBundle` at `manager.go:756`, so a hostile `github.com/<attacker>/pkg` install plants symlinks, escapes staging, or bombs disk. Same pattern in `internal/ide/ideupgrade/extract.go:101`.
2. **Public dep-bump PR** — `oras.land/oras-go/v2` 2.6.1 → 2.6.2 patches GHSA-fxhp-mv3v-67qp (High), GHSA-m37j-52j7-pjw7 (High), GHSA-h7vf-4x9w-h99v (Moderate SSRF on rune's `FetchManifest` path), GO-2026-5880.

**Dropped with reasoning** (in the article): goldmark 1.7.1 XSS (AST-only usage), imaging 1.6.2 (no fix upstream), x/crypto openpgp (unused), x/mod (toolchain-fixed, Go 1.26.6 already past), insomniacslk/dhcp (indirect via tailscale), SSH `InsecureIgnoreHostKey` (opt-in flag), `e2e.yml` curl-pipe-shell (CI-only).

**Files created/modified:**
- `.pending-disclosure/unstablebuild-rune-2026-09-19T164400Z-pvr.md` (new)
- `.pending-disclosure/unstablebuild-rune-2026-09-19T164400Z-deps.md` (new)
- `articles/vuln-scan-2026-09-19.md` (new)
- `.outputs/vuln-scanner.md` (refreshed)
- `memory/vuln-scanned.json` (appended, `runs=15`)
- `memory/logs/2026-09-19.md` (appended `### vuln-scanner` block)
- `.pending-notify/1789836429-vuln-scanner.md` (drafted, operator postprocess fans out)

**Follow-up:** Operator to submit the PVR (advisory form or `security@unstable.build`) and the public `oras-go` bump PR from a workstation identity — the GitHub-App identity cannot fork per `[[github-app-cannot-fork-third-party-repos]]`. Dedup entry expires 2026-10-19.
