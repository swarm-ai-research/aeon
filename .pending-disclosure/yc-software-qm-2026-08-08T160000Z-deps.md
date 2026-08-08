# Dependency-CVE PR draft — yc-software/qm

**Status:** DRAFT — pending operator submission as a public PR.

**Target commit:** `0f0e0adccce2d13e4aff3e5bf3efb0cccf312f7a`
**Detected:** 2026-08-08 via Aeon vuln-scanner (osv-scanner 2.5.0)

Aeon (the aeonframework GitHub App) cannot fork `yc-software/qm` from a
GitHub-App integration context (HTTP 403 on `POST /repos/.../forks`). This
draft records the PR body + the concrete lockfile actions so the operator can
open the PR from a user account.

Suggested branch: `security/bump-deps-2026-08-08`
Suggested title: `fix(deps): bump 9 packages to patch 21 disclosed advisories`

---

## PR body (paste as-is)

Automated dependency bumps to address disclosed CVEs / GHSAs. Detected by
[osv-scanner](https://google.github.io/osv-scanner/). No code changes outside
`package-lock.json`; every direct dep in `package.json` remains at its declared
range — the bumps land at transitive/lockfile level via `npm audit fix` (or
`npm update <pkg>` where audit-fix over-widens).

### Root `package-lock.json`

| Package | Current | Fixed in (min) | Advisories |
|---|---|---|---|
| `brace-expansion` | 5.0.8 | 5.0.9 | GHSA-rgw5-rvv9-x895 (HIGH) — DoS via unbounded intermediate arrays, bypasses CVE-2026-14257 mitigation |
| `fast-uri` (v3) | 3.1.4 | 3.1.5 | GHSA-7p8r-x3mc-p8w7 (HIGH) — host confusion via backslash authority introducer |
| `fast-uri` (v4) | 4.1.1 | 4.1.2 | GHSA-7p8r-x3mc-p8w7 (HIGH) |
| `hono` | 4.12.32 | 4.12.34 | GHSA-54fx-42gc-7vw4 (algo-DoS in Language MW), GHSA-79qm-7rj5-m7r9 (Proxy Helper leaks `Connection` headers), GHSA-8j4g-w8fx-2239 (ReDoS in CORS MW), GHSA-f23p-vx2j-j53r (`memo()` retains SSR output across requests — **cross-user data disclosure**) |
| `undici` | 8.5.0 | 8.9.0 | GHSA-4cwx-7wf7-3272 (cross-user info disclosure via private cache directives), GHSA-8xcm-r25x-g524 (downstream response desync via retry interceptor), GHSA-jr45-8vmc-qm54 (cross-user info disclosure via whitespace in Cache-Control), GHSA-m8rv-5g2x-5cg5 (CRLF injection via blob body `type`), GHSA-v3r7-h72x-cjcm (cookie attribute injection) |

### `plugins/web-ui/package-lock.json`

| Package | Current | Fixed in (min) | Advisories |
|---|---|---|---|
| `dompurify` | 3.4.12 | 3.4.13 | GHSA-55q2-fjhq-7xh7 (MODERATE) — IN_PLACE hook removal leaves detached subtree executable, causing XSS |
| `nanoid` | 3.3.12 | 3.3.16 | GHSA-28wg-ghj8-5hjv (HIGH) — non-secure generators loop indefinitely with negative size; GHSA-2v37-7h3g-55p8 — same class for size=0 |
| `postcss` | 8.5.18 | 8.5.23 | GHSA-fxqj-rqcc-2cmp (MODERATE) — incomplete fix of GHSA-6g55-p6wh-862q; attacker-controlled `sourceMappingURL` reads arbitrary `.map` files |
| `undici` | 7.28.0 | 7.29.0 | same 5 GHSAs as root |

That's **9 unique lockfile bumps** covering **21 distinct advisories**
(the `undici` bumps are counted once each — same 5 advisories on both).

### Special case: `xlsx@0.20.3`

`osv-scanner` also flags `xlsx@0.20.3` in `plugins/web-ui/package-lock.json`
for two SheetJS advisories that **have no fix version** in npm:

- GHSA-4r6h-8v6p-xvw6 — Prototype Pollution
- GHSA-5pgg-2g8v-p4x9 — ReDoS

SheetJS discontinued npm-registry releases in 2023; the maintained builds are
distributed from `cdn.sheetjs.com`. `xlsx` is not a direct dep — the lockfile
shows it pulled in via `node_modules/@earendil-works/pi-web-ui` (an upstream
package under the yc-software org). **This bump requires an upstream fix in
`@earendil-works/pi-web-ui` first** — either replacing `xlsx` with an
alternative parser or migrating to the CDN build. This PR does not attempt the
xlsx bump; tracking it as a follow-up is safer than shipping a lockfile hack.

### Suggested command sequence

```bash
# root
npm audit fix --package-lock-only
# if audit-fix skips any of the above (locked by ranges), targeted updates:
npm update brace-expansion fast-uri hono undici

# plugins/web-ui
cd plugins/web-ui
npm audit fix --package-lock-only
npm update dompurify nanoid postcss undici
```

Then verify:

```bash
npm run typecheck
npm run lint
# and the tests that exercise the affected surfaces —
# hono routing, undici HTTP client, dompurify sanitization
```

---

## Metadata

- **Repo:** yc-software/qm (`0f0e0adccce2d13e4aff3e5bf3efb0cccf312f7a`)
- **Scanner:** osv-scanner 2.5.0
- **Total vulnerable packages:** 10 (9 fixable now, 1 blocked on upstream)
- **Total distinct GHSAs:** 12 (5 shared between two undici lockfile entries)
- **Filed by:** [Aeon](https://github.com/aeonframework/aeon)
