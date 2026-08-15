All artifacts landed. Skill run complete.

## Summary

Ran `vuln-scanner` for 2026-08-15 against `SMNETSTUDIO/WeChat-AI` (1,730★, TypeScript monorepo, HEAD `1f56c7f`; a 5-day-old trending self-hosted WeChat roleplay bot service). Selection passed 30-day dedup + PVR+SECURITY.md safe-channel check.

**Confirmed: 3 code findings + 5 fixable dep bumps covering 23 CVEs.**

- **Code F1 (MEDIUM, SSRF):** DNS-rebinding TOCTOU in `huggingface/wechat-ai-tools/services/security.py` — `socket.getaddrinfo()` validates non-private, `httpx.AsyncClient` re-resolves and connects to whatever DNS returns second. Attacker with a valid `TOOLS_API_KEY` (default: any main-site user with a custom-LLM configured) can exfiltrate cloud metadata through the gateway.
- **Code F2 (LOW):** AES-256-GCM `createDecipheriv` without pinned `authTagLength` in `packages/db/src/secret-crypto.ts:72` — same class as prior yc-software/qm finding.
- **Code F3 (LOW, deployment-conditional):** `apps/api/src/routes.ts:324-331` `clientIp()` unconditionally trusts `cf-connecting-ip`/`x-forwarded-for` — rate-limit bypass when API is exposed directly.
- **Deps:** starlette 0.46.2→1.3.1 (14 CVEs), fast-uri 3.1.3+4.1.0 → 3.1.5+4.1.2, find-my-way 9.6.0→9.7.0, idna 3.9.0→3.15, pytest 8.3.5→9.0.3 (dev). 0 verified secrets fs + git.
- **Discarded 4 semgrep candidates** as false-positive/design/test-file after per-hit code review; also manually reviewed OAuth, OTA-apply, sticker security, chatflow HTTP node, admin authz — all clean, well-defended.

**Files:** `articles/vuln-scan-2026-08-15.md`, `memory/vuln-scanned.json` (+1, 10th run), `.pending-disclosure/SMNETSTUDIO-WeChat-AI-2026-08-15T163000Z-{pvr,deps}.md`, `.pending-notify/1786812282-vuln-scanner.md`, `memory/logs/2026-08-15.md` (appended `vuln-scanner` entry).

**Follow-up:** Both PVR + deps-PR drafts hold for operator out-of-band submission (Aeon App can't fork third-party repos from cron per [[github-app-cannot-fork-third-party-repos]]; PVR endpoint verified enabled). Next vuln-scanner picks a fresh target on 2026-08-22. Repo dedup-locked until 2026-09-14.
