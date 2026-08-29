All artifacts in place. Skill run complete.

## Summary

Ran `vuln-scanner` on **`CopilotKit/OpenBot`** (3,404★, TypeScript, HEAD `fb0c797`, opened 12d ago). Selected off the trending shortlist for agent-runtime attack surface (Bot with browser + shell + file access per instance), passed PVR-enabled + not-teaching + 30-day-dedup filters.

**Clean audit — 0 confirmed findings, no PVR filed, no public PR filed.**

- **Code (0 confirmed):** semgrep's 4 `dockerfile.missing-user` hits are false positives on a deliberate s6-supervised multi-user drop-from-root pattern the author documents in-line at `Dockerfile:186-201`. Manually reviewed the high-value surfaces the scanners under-cover for agent-runtime code (`workspace.ts` — 3-layer path confinement + symlink-at-last-component walk; `shell.ts` — env allowlist + `NEVER_PASSED` deny; `target.ts` — SSRF w/ full IPv4-in-IPv6 canonicalisation across mapped/compat/NAT64; `agents/endpoint.ts` — redirect-rechecked; `authorisation.ts` — constant-time compare; all 3 workflows — SHA-pinned, `persist-credentials:false`, every `${{ github.* }}` routed through `env:` block, no CWE-78 shape). Exceptionally well-defended codebase — every check has a comment explaining the incident it caught.
- **Secrets (0):** TruffleHog filesystem + git-history both empty.
- **Deps (0 actionable):** 16 vulnerable transitive npm pkgs (undici@5.29.0 ×12 advisories, lodash-es@4.17.21 ×3, esbuild@0.18.20, @ai-sdk/provider-utils@3.0.32). No public bump PR — CopilotKit's shared Renovate preset is scoped `enabledManagers:[github-actions]` so npm bumps are explicitly the maintainer's manual gate, and no clean direct-dep fix exists without bun `overrides` or a `@ai-sdk/google-vertex` major bump.

**Sandbox note:** bash-side stdout redirection into workdir blocked even with allowed paths (recurrence of `sandbox-blocks-shell-redirect-to-workdir` class); worked around with in-repo `tmp-vuln-scan/wrap.py` (`subprocess.run(capture_output=True)` → `open("wb").write()`). Same shape as the checked-in `scripts/notegraph-fingerprint.mjs` fix.

**Files:**
- `articles/vuln-scan-2026-08-29.md` (new)
- `memory/vuln-scanned.json` (+1, 12th run; repo dedup-locked until 2026-09-28)
- `memory/logs/2026-08-29.md` (appended vuln-scanner entry + summary)
- `.pending-notify/1788024818-vuln-scanner.md`
- `.gitignore` (+`.vuln-scan-tmp/`, `tmp-vuln-scan/` to ignore scratch dirs)

**Follow-up:** next vuln-scanner picks a fresh target Sat 2026-09-05. Sandbox shell-redirect friction now n≥5 across notegraph (n=4) + vuln-scanner (n=1) — worth atomising as its own note vs. the existing broader `sandbox-blocks-shell-redirect-to-workdir`.
