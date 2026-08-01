---
kind: public-pr-dependency-bumps
target_repo: talivia-group/talivia
target_head: 8248ccf3333b9d490712b53a87806abb2e2541cf
detected_at: 2026-08-01T16:00:00Z
detected_by: aeon (osv-scanner v2.4.0)
submit_via: gh repo fork talivia-group/talivia && … && gh pr create
blocked_by: github-actions-cannot-create-prs (see memory index)
---

# Public PR draft — bump direct deps to patch disclosed CVEs

All findings below are **already-public** advisories (GHSA + CVE IDs
assigned). Public PRs are the correct channel per the vuln-scanner routing
table: dependency CVEs are net-positive to fix in the open.

## Direct-dependency bumps recommended (one PR each; keep them isolated for
easy review)

### 1. `next` `16.2.6` → `16.2.11`   **[9 GHSAs, several HIGH]**

Manifest line: `package.json:91` — `"next": "16.2.6"` (exact pin, not a
caret).

CVEs addressed by 16.2.11:

| GHSA | CVE | Severity | Summary |
|---|---|---|---|
| GHSA-89xv-2m56-2m9x | CVE-2026-64649 | **HIGH** | SSRF in Server Actions on custom servers |
| GHSA-p9j2-gv94-2wf4 | CVE-2026-64645 | **HIGH** | SSRF in rewrites via attacker-controlled destination hostname |
| GHSA-6gpp-xcg3-4w24 | CVE-2026-64642 | **HIGH** | Middleware / Proxy bypass in App Router w/ Turbopack + single locale |
| GHSA-m99w-x7hq-7vfj | CVE-2026-64641 | **HIGH** | DoS in App Router using Server Actions |
| GHSA-955p-x3mx-jcvp | CVE-2026-64643 | MODERATE | Unauthenticated disclosure of internal Server Function endpoints |
| GHSA-4c39-4ccg-62r3 | CVE-2026-64646 | MODERATE | Unbounded Server Action payload in Edge runtime |
| GHSA-4633-3j49-mh5q | CVE-2026-64647 | MODERATE | Cache confusion of response bodies (invalid UTF-8 byte sequences) |
| GHSA-68g3-v927-f742 | CVE-2026-64648 | MODERATE | Cache confusion of response bodies (with bodies) |
| GHSA-q8wf-6r8g-63ch | CVE-2026-64644 | MODERATE | DoS in Image Optimization API via SVGs |

**Manifest patch:**
```diff
--- a/package.json
+++ b/package.json
@@ -88,7 +88,7 @@
-    "next": "16.2.6",
+    "next": "16.2.11",
```
Regenerate `pnpm-lock.yaml` with `pnpm install`.

**PR title (suggested):**
`fix(deps): bump next to 16.2.11 to patch CVE-2026-64641..64649`

**PR body (suggested):**
```
Automated dependency bump to address nine disclosed advisories in Next.js.
The highest-severity items are two SSRF vectors (CVE-2026-64645 in rewrites
with attacker-controlled destination hostname; CVE-2026-64649 in Server
Actions on custom servers) and a middleware bypass in App Router
(CVE-2026-64642). All addressed by the patch release.

Detected by osv-scanner (Google) against pnpm-lock.yaml at HEAD
8248ccf3. No code changes outside package.json / pnpm-lock.yaml.

Advisory index:
https://github.com/vercel/next.js/security/advisories

Filed by Aeon (https://github.com/aeonframework/aeon).
```

---

### 2. `sharp` `^0.34.5` → `^0.35.0`   **[HIGH, inherited libvips CVEs]**

Manifest line: `package.json:112` — `"sharp": "^0.34.5"` (caret; the current
range does NOT include 0.35.x).

CVE addressed:

| GHSA | Severity | Summary |
|---|---|---|
| GHSA-f88m-g3jw-g9cj | **HIGH** | sharp inherited vulnerabilities in libvips: CVE-2026-33327, CVE-2026-33328, CVE-2026-35590, others |

**Manifest patch:**
```diff
--- a/package.json
+++ b/package.json
@@ -109,7 +109,7 @@
-    "sharp": "^0.34.5",
+    "sharp": "^0.35.0",
```
Regenerate lockfile. Verify Image Optimization still functions
(`sharp` is Next.js's default image pipeline).

**PR title (suggested):**
`fix(deps): bump sharp to ^0.35.0 to patch inherited libvips CVEs (GHSA-f88m-g3jw-g9cj)`

---

### 3. `ua-parser-js` `^2.0.9` → `^2.0.10`   **[MODERATE ReDoS]**

Manifest line: `package.json:115` — `"ua-parser-js": "^2.0.9"`.

The current caret range accepts `2.0.10`, so this is a lockfile-only
refresh in principle; but osv-scanner sees `2.0.9` in the lock, so a
`pnpm update ua-parser-js` (or `pnpm install`) is needed to actually pull in
2.0.10.

CVE addressed:

| GHSA | CVE | Severity | Summary |
|---|---|---|---|
| GHSA-9h5v-pfqq-x599 | CVE-2026-48125 | MODERATE | Unbounded `Sec-CH-UA-Model` parsing can trigger ReDoS in `withClientHints()` |

**PR title (suggested):**
`fix(deps): refresh ua-parser-js to 2.0.10 to patch CVE-2026-48125 (ReDoS)`

Combine with #4 below if bundling.

---

### 4. `postcss` `^8.5.10` → `^8.5.18` (lockfile refresh) + `esbuild` `^0.27.4` → `^0.28.1` (optional, low)

- `postcss`: caret already accepts 8.5.18. Lock currently pins two versions
  (8.4.31 and 8.5.14, both transitive-affected by GHSA-r28c-9q8g-f849, path
  traversal in Previous Source Map Auto-Loading). `pnpm update postcss` or a
  lockfile regen brings both instances current.
- `esbuild`: HIGH-only-on-Windows dev-server file read (GHSA-g7r4-m6w7-qqqr).
  Low priority; safe to bundle in the same lockfile-refresh PR or skip.

**PR title (suggested):**
`fix(deps): refresh postcss and esbuild lockfile entries to patch
GHSA-r28c-9q8g-f849 and GHSA-g7r4-m6w7-qqqr`

---

## NOT recommended right now

- **`undici` 7.25.0 → 8.5.0** — major-version bump (7.x → 8.x) with API
  changes. Transitive dep only; leave for a maintainer-led upgrade.
- **`hono` 4.12.9 → 4.12.27** (23 GHSAs) — transitive only, pulled in by
  another dep (`@hono/node-server`); needs the intermediate to bump first.
  Not directly bumpable.
- **`brace-expansion`, `minimatch`, `js-yaml`, `yaml`, `svgo`, `picomatch`,
  `serialize-javascript`, `shell-quote`, `fast-uri`, `defu`, `d3-color`,
  `valibot`, `vite`, `@babel/core`, `@isaacs/brace-expansion`, `diff`** —
  all transitive. Wait for their consumers to bump, or file separately with
  the transitive consumer if strategic.

## Submission workflow (blocked)

Direct submission from Aeon is currently blocked by
`github-actions-cannot-create-prs` (see MEMORY.md index). Operator path:

```bash
# From a machine with a GH token that has repo:public + workflow scopes:
gh repo fork talivia-group/talivia --clone --default-branch-only -- --depth 200
cd talivia
git checkout -b security/bump-next-16.2.11

# Edit package.json line 91: "next": "16.2.6" → "16.2.11"
pnpm install     # regenerates pnpm-lock.yaml

git add package.json pnpm-lock.yaml
git commit -m "fix(deps): bump next to 16.2.11 to patch CVE-2026-64641..64649

Advisory index: https://github.com/vercel/next.js/security/advisories
Severity: High (SSRF in rewrites + Server Actions)
Fixed in: 16.2.11"

git push -u origin HEAD

gh pr create --repo talivia-group/talivia \
  --title "fix(deps): bump next to 16.2.11 to patch CVE-2026-64641..64649" \
  --body-file <(sed -n '/^\*\*PR body (suggested):\*\*/,/^```$/p' \
                    .pending-disclosure/talivia-group-talivia-2026-08-01T160000Z-deps.md \
                | sed '1d;$d;1d;$d')

# Repeat for sharp, ua-parser-js, postcss+esbuild — one branch + PR each.
```

Once [[github-actions-cannot-create-prs]] is unblocked (operator toggle or
AEON_GH_PAT), this can move to auto-submission.
