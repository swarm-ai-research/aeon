*Vuln Scanner — NVlabs/SoL-Pi* (1,404★, TypeScript, NVIDIA pi-coding-agent extension)
1 confirmed finding: dep CVE **GHSA-82fw-gwwq-j7x9 / CVE-2026-84373** (medium, CWE-22 path traversal) in vitest 4.1.9 + @vitest/mocker 4.1.9 — dev-only devDependency, fixed in 4.1.11.
0 code vulns, 0 verified secrets, well-defended (Semgrep silent; SECURITY.md discloses attack surface; safePiBashTempPath in evidence-preserving-reducer defensively narrowed).
Disclosed via: **public-PR drafted** (`.pending-disclosure/NVlabs-SoL-Pi-2026-09-12T161500Z-deps.md`) — not auto-pushed, operator submits per github-app-cannot-fork-third-party-repos.
Scanners: semgrep=ok, trufflehog=ok, osv=ok, slither=n/a (no .sol).
