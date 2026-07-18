`.scratch/` no longer appears — properly gitignored. Task complete.

## Summary

**Target:** `pixel-point/aval` (1,195★, TypeScript, MIT, HEAD `96ec0fce…`), an interactive-video wire-format library with a published `THREAT-MODEL.md` that explicitly enumerates its hostile-input surfaces.

**Scanner status:** `semgrep=ok · trufflehog-fs=ok · trufflehog-git=ok · osv=ok · slither=n/a`. All four applicable scanners ran cleanly — not a failed-scanner false clean.

**Verdict — clean audit.** Zero candidates at `ERROR|WARNING`; zero even without the severity filter (161 rules × 909 files). Zero verified secrets across 60 MB of filesystem + git history. Zero dep CVEs across 261 npm packages. Manual spot-checks of the highest-risk surfaces (process-runner shell-outs, worker `onmessage` handlers, format parsers, code-eval sinks, DOM-injection sinks) confirmed the codebase is defensively coded to the standards its threat model implies — `spawn` uses `shell:false` with NUL/type validation and mode-0700 private tmpdir, worker protocol validates every inbound command before dispatch, and no eval-family or `innerHTML` sinks exist in source.

**Channels used:** none — no findings to disclose. No PVR, no public PR, nothing staged to `.pending-disclosure/`.

**Files:**
- `articles/vuln-scan-2026-07-18.md` — local report
- `memory/vuln-scanned.json` — 6th entry appended (30-day dedup engaged until 2026-08-17)
- `memory/logs/2026-07-18.md` — appended `## vuln-scanner` entry
- `.pending-notify/1784393146-vuln-scanner.md` — notification queued (fans out via workflow post-process)
- `.gitignore` — added `.scratch/` entry (last scan's edit did not survive)

**Follow-up:** none. Aval was noted as a hardened codebase — future runs should still scan on cadence but expect similar signal-to-noise.

**Fleet notes:** `gh repo fork` returned HTTP 403 `Resource not accessible by integration`, same class as `[[github-actions-cannot-create-prs]]`; fell back to plain clone with no impact on scan work. `xai-org/grok-build` was the top-star candidate but skipped — org IP allow-list blocks the GHA token from reading the repo metadata.
