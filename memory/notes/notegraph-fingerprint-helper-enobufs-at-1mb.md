---
id: notegraph-fingerprint-helper-enobufs-at-1mb
created: 2026-09-17
type: lesson
links: [[notegraph-fingerprint-pipeline-blocked-by-sandbox]], [[notegraph-workspace-head-diverges-from-origin]]
---
# The notegraph fingerprint helper's default `execSync` maxBuffer overflows when reading HEAD `notegraph.json` past ~1 MB, silently truncating the delta computation

**Why:** on the 09-17 notegraph dispatch the ad-hoc `/tmp/notegraph-fingerprint.mjs` helper (already required per [[notegraph-fingerprint-pipeline-blocked-by-sandbox]] because sandbox blocks the shell pipeline) hit `ENOBUFS` when reading HEAD `notegraph.json` at ~1 MB — Node's default `execSync` `maxBuffer` is 1 MiB, and the current graph has grown past it (~1.05 MB at 389n/3088h). Left uncaught this manifests as either an exception (as today) or, in `spawn` code paths that swallow ENOBUFS, silent truncation of the stdout buffer which corrupts the delta.

**How to apply:** the durable fix is to bump `maxBuffer` to 128 MiB in whichever node helper ships alongside `scripts/notegraph.mjs` (the checked-in successor to the ad-hoc helper). Any future skill that reads the graph JSON via `execSync`/`spawnSync` needs the same treatment; prefer `readFileSync` when the target is a file (no buffer limit) rather than `git show HEAD:path | node -e '…'`. Bundle with the `scripts/notegraph-fingerprint.mjs` fix already queued per [[notegraph-fingerprint-pipeline-blocked-by-sandbox]].
