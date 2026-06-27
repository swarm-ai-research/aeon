Leaving the 26MB scratch dir for janitor to clean up — running rm on a workspace path requires explicit approval. Wrapping up.

## Summary

Ran the **vuln-scanner** skill against `vercel/eve` (2,771⭐, TypeScript, head `faf86e30`).

**Result:** clean code surface, dependency CVE backlog drafted for operator-side disclosure.

- **Code SAST** (semgrep, 1,695 files): **0 findings** at WARNING+ severity.
- **Verified secrets** (trufflehog filesystem + git, 11.5k chunks): **0**.
- **Dependency CVEs** (osv-scanner, 2,347 packages): **72 GHSA advisories across 28 packages** — but the `eve` package's only runtime dep is `nitro`, which is unaffected. All flagged CVEs are in dev tooling (vite/esbuild/postcss), the Nuxt framework integration, the docs site's mermaid transitive (`dompurify@3.4.5` × 8 bypasses), HTTP transitives (`undici` × 18, `tar` × 4), and e2e fixtures (`@opentelemetry/core@2.6.1` × 11 fixtures).
- **Slither**: n/a (no `.sol`).

**Disclosure**: 1 bundled public-PR draft staged at `.pending-disclosure/vercel-eve-2026-06-27T160000Z.md` — direct-dep bumps (`nuxt 4.4.6→^4.4.7`, `vite ^8.0.5`, `@opentelemetry/core ^2.8.0`) plus `pnpm.overrides` for the worst transitives. Operator must submit because the Aeon App token still can't fork external repos (HTTP 403, same as the 2026-06-20 omnigent run). Repo enforces DCO + signed commits — operator needs `git commit -s` from a GPG-verified branch.

**Files created/modified:**
- `articles/vuln-scan-2026-06-27.md` — full report
- `.pending-disclosure/vercel-eve-2026-06-27T160000Z.md` — drafted PR contents
- `memory/vuln-scanned.json` — `vercel/eve` dedup entry through 2026-07-27
- `memory/logs/2026-06-27.md` — appended `### vuln-scanner` section
- `.pending-notify/1782579501.md` — notification staged for post-run delivery

**Operator follow-up:**
1. Fork `vercel/eve` from a personal account and apply the bundled bumps from `.pending-disclosure/vercel-eve-2026-06-27T160000Z.md`.
2. Investigate the `sandbox@3.1.2` transitive (npm name, not `@vercel/sandbox`) — flagged as "sandbox breakout / arbitrary code execution" with no upstream fix; needs `pnpm why sandbox` to identify which dep is pulling it.
3. The App's missing fork scope remains the recurring blocker — same as 2026-06-20.
4. 26MB of scratch (`scan-cache/`, `.vuln-scan-*/`) left behind because `rm` on workspace paths needs explicit approval; janitor can clean up.
