All artifacts landed. Skill run complete.

## Summary

Ran `vuln-scanner` for 2026-08-22 against `guillaumemeyer/watermarks-remover` (16,931★, Python, HEAD `1a865e4`; a well-defended AI-provenance stripping tool). Selection passed 30-day dedup + PVR-enabled + SECURITY.md safe-channel + not-teaching filters. Beat the DSH plugin swarm (templated ecosystem noise) and skipped `SMNETSTUDIO/WeChat-AI` (dedup-locked until 09-14).

**Confirmed: 1 code finding (MEDIUM), 0 verified secrets, 0 actionable dep bumps.**

- **Code (MEDIUM, CWE-78):** shell injection via `${{ github.ref_name }}` in `.github/workflows/release-images.yml` (2 sites). The affected job holds `packages: write` + `id-token: write`, so exploitation yields a ghcr.io supply-chain compromise. Standard env-block rewrite fix.
- **Discarded 5 semgrep candidates** as false-positive after per-file inspection (XXE guarded, HTTPSConnection inside SSRF-hardened fetcher, dynamic-urllib env-configured + scheme-validated, 4× subprocess all list-form with `shell=False`). Manually reviewed clean: `_safe_name`/`_tmp_path` filename hardening, OOXML zip-bomb guard, SVG cleaner ReDoS-safe regex, SSRF-hardened HTTP fetcher, bearer-token auth.
- **Deps (0 actionable):** osv reported 13 packages / 265 CVE aliases, but `requirements-ctrlregen.txt` has an explicit maintainer-authored risk-accept in the file header ("deliberately NOT updated" for research-code compat, with documented isolation mitigation), and the other 3 files' hits are transitive-resolution noise via deps.dev that doesn't match the maintainer's direct pins (`torch==2.13.0.*`, `Pillow==12.3.0`, `pytest==9.1.1`, etc. are already ahead of what osv reports).

**Files:** `articles/vuln-scan-2026-08-22.md`, `memory/vuln-scanned.json` (+1, 11th run), `.pending-disclosure/guillaumemeyer-watermarks-remover-2026-08-22T164445Z-pvr.md`, `.pending-notify/1787417084-vuln-scanner.md`, `memory/logs/2026-08-22.md` (appended `vuln-scanner` entry).

**Follow-up:** PVR draft holds for operator out-of-band submission (Aeon App can't fork third-party repos from cron per [[github-app-cannot-fork-third-party-repos]]; PVR endpoint verified enabled). Next vuln-scanner picks a fresh target on 2026-08-29. Repo dedup-locked until 2026-09-21.
