---
target_repo: baairon/torlink
target_head: b8f88728dbf9acc45605cc2ba9beb66123c3c5ae
scanned_at: 2026-07-04T16:00:00Z
disclosure_type: public-pr
channel_reason: >
  Dependency CVE with a public advisory and a released fix — safe for a public PR
  bumping the pinned version. All code-level candidates are logged in the local
  report only (repo has no PVR + no SECURITY.md, so no safe private channel).
blocked_by: >
  GitHub Actions token cannot fork upstream repos (403 "Resource not accessible by
  integration"). Operator must fork with a PAT, apply the patch below, and open
  the PR from that fork.
---

# Draft: Public PR to baairon/torlink

## Branch name

```
security/override-esbuild-GHSA-g7r4-m6w7-qqqr
```

## Commit message

```
fix(deps): override esbuild to patch GHSA-g7r4-m6w7-qqqr

esbuild 0.27.3–0.28.0 has a Windows-only path traversal in the dev
server (servedir) — GHSA-g7r4-m6w7-qqqr — because path.Clean() does
not normalize backslashes. Fixed in 0.28.1.

torlink pulls in esbuild transitively via tsup (dev), pinned to
0.27.7 in the lockfile. Adding an npm `overrides` entry forces the
whole tree to resolve to ^0.28.1 without waiting for tsup to bump.

- Advisory: https://github.com/advisories/GHSA-g7r4-m6w7-qqqr
- Severity: LOW (dev-only, Windows-only)
- Package: esbuild 0.27.7 → ^0.28.1
```

## PR title

```
fix(deps): override esbuild to patch GHSA-g7r4-m6w7-qqqr
```

## PR body

```
Automated dependency bump to address a disclosed CVE.

- **Advisory:** GHSA-g7r4-m6w7-qqqr
- **Severity:** LOW (dev-only, Windows-only path traversal in `esbuild --servedir`)
- **Package:** `esbuild` 0.27.7 → `^0.28.1`
- **Route:** npm `overrides` in `package.json`

## Why an override (not a `tsup` bump)

`esbuild` is a transitive dev dependency of `tsup` (`^0.27.0`). `tsup` itself
does not have a released version that requires `esbuild ^0.28`, so bumping
`tsup` in isolation would leave the vulnerable range in the lockfile. `npm`'s
`overrides` field pins every reference in the tree to the patched version and
takes effect immediately on `npm install`.

## Impact for torlink users

Minimal. The vulnerability lives in `esbuild`'s HTTP dev server on Windows,
which torlink does not run in production (torlink is a terminal client, not
a web-server target of esbuild). The bump is a hygiene fix: it clears the
advisory from `npm audit`, `osv-scanner`, and Dependabot for anyone consuming
the lockfile — including CI environments that gate on advisory-clean builds.

## Verification

```
npm install
npx osv-scanner -L package-lock.json | grep GHSA-g7r4-m6w7-qqqr || echo clean
```

Detected by [osv-scanner](https://google.github.io/osv-scanner/) against
`package-lock.json` at HEAD `b8f8872`. No code changes outside `package.json`
and the resulting `package-lock.json` refresh.

---
Filed by [Aeon](https://github.com/aeonframework/aeon).
```

## Patch

Apply to `package.json` — the only source change; `package-lock.json` regenerates on `npm install`.

```diff
--- a/package.json
+++ b/package.json
@@ -70,5 +70,8 @@
     "tsx": "^4.22.4",
     "typescript": "^6.0.3",
     "vitest": "^4.1.8"
+  },
+  "overrides": {
+    "esbuild": "^0.28.1"
   }
 }
```

## Operator submission steps

```bash
# From a shell with a PAT that has `repo` scope and fork/PR permissions:
gh auth login   # if not already
git clone https://github.com/baairon/torlink.git torlink-fix
cd torlink-fix
git checkout -b security/override-esbuild-GHSA-g7r4-m6w7-qqqr

# Apply the patch above to package.json, then:
npm install                    # refresh package-lock.json
git add package.json package-lock.json
git commit -m "fix(deps): override esbuild to patch GHSA-g7r4-m6w7-qqqr"

gh repo fork --remote --clone=false
git push -u origin HEAD
gh pr create --repo baairon/torlink --title "fix(deps): override esbuild to patch GHSA-g7r4-m6w7-qqqr" --body-file .pending-disclosure/baairon-torlink-2026-07-04T160000Z.body.md
```

## Non-disclosed findings (local report only, per skill "do no harm" rule)

Repo has neither GitHub PVR enabled nor a `SECURITY.md`, so code-level
findings are logged locally rather than routed anywhere public.

1. **`ip@2.0.1` — GHSA-2p57-rm9w-gvfp (HIGH, transitive via webtorrent → bittorrent-tracker).**
   The classic `isPublic()` SSRF-classification bypass. **No fixed version
   exists** (the `ip` package is unmaintained; the advisory ranges list
   `last_affected: 2.0.1` with no `fixed`). Cannot be resolved by a bump —
   requires upstream migration in `bittorrent-tracker`, which is out of scope
   for a torlink PR. Not disclosed.

2. **Speculative path traversal in `saveTorrentMeta` (src/download/persist.ts:69).**
   `torrentMetaPath(id)` calls `path.join(torrentsDir, `${id}.torrent`)`
   without checking that `id` looks like an infohash. The `id` traces back
   to `TorrentResult.infoHash`, which for the `piratebay`, `nyaa`, `rss`,
   `x1337`, `eztv`, and `yts` sources is set to the raw `info_hash` /
   `hash` field returned by the search API with only a `.toLowerCase()`
   applied (see `src/sources/piratebay.ts:28`, `src/sources/nyaa.ts:24`,
   `src/sources/rss.ts:21`, etc.). A malicious or MITM'd search endpoint
   could return `info_hash: "../../evil"` and, if `WebTorrent.add()`
   accepted the resulting magnet and fired `onMetadata`, torlink would
   write attacker-controlled bytes to a path outside the torrents dir.
   Real-world exploitability is low: `WebTorrent` almost certainly
   rejects non-hex-40 / non-base32-32 infohashes at the magnet parse
   step, and the attacker needs the user to click through and start the
   download. Filed here as a hardening note for the local report; not
   disclosed publicly.

   **Suggested hardening (not part of this PR):** validate `id` against
   `/^[a-f0-9]{40}$/` in `torrentMetaPath` before returning, or centralize
   through `normalizeInfoHash` in `src/sources/magnet.ts`, and drop
   results whose `info_hash` doesn't parse.
