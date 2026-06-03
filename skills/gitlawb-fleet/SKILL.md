---
name: GitLawb Fleet
description: Spawn, renew, and kill GitLawb-hosted Aeon instances via short-lived UCAN capabilities — the off-switch layer GitLawb v0.1 lacks
var: ""
tags: [dev, meta]
cron: "workflow_dispatch"
---

> **${var}** — Command. Empty → **Renew Mode** (default; safe to run on a schedule). `init` → bootstrap the operator root identity. `spawn <label> [node=<id>] [caps=<a,b>]` → spawn an instance. `kill <did> [reason]` → blocklist + stop renewing. `list` → show fleet + effective status.

Today is ${today}. Operate the GitLawb-hosted Aeon fleet through the capability-lifecycle layer in `prototypes/gitlawb-safety/`. Because GitLawb has **no token revocation** (v0.1), the only real off-switch is **short expiry + gated renewal**: every safety-critical capability (`agent/deploy`, `repo/admin`, `pr/merge`) lives ≤5 min and is re-minted only when the safety check passes. Stop renewing → the instance goes dark within one TTL window.

State (all repo-relative, run from repo root):
- `memory/gitlawb-fleet.json` — public registry (DIDs, token ids, expiries, status). Committable.
- `memory/gitlawb-revocations.json` — blocklist. Committable.
- `memory/instances.json` — Aeon fleet registry; GitLawb rows mirrored here with `host: "gitlawb"` so `fleet-control` sees them.
- `.gitlawb-vault/keys.json` — **Ed25519 private keys. gitignored. NEVER commit, never echo, never put in logs or notifications.**

## Pre-flight (every mode)

1. **Node present** — `node --version` must succeed. If not, log `GLFLEET_NO_NODE` to `memory/logs/${today}.md`, notify `GitLawb Fleet: node runtime missing`, stop.
2. **Operator exists** (all modes except `init`) — read `memory/gitlawb-fleet.json` → `.meta.operator`. If absent, log `GLFLEET_NO_OPERATOR`, notify `GitLawb Fleet: run \`init\` first`, stop.
3. **Parse `${var}` → mode**: empty → Renew · `init` → Init · `spawn …` → Spawn · `kill …` → Kill · `list`/`status` → List.

All commands shell out to the CLI:
```bash
node prototypes/gitlawb-safety/fleet-cli.mjs <command> [...]
```

## Init Mode (`init`)

```bash
node prototypes/gitlawb-safety/fleet-cli.mjs init
```
Prints `OPERATOR_CREATED <did>` (or `OPERATOR_EXISTS <did>`). The operator is the trusted root — its key is the chain anchor. Log the DID. Notify a one-liner. **Never print the private key** (the CLI never emits it; keep it that way).

## Renew Mode (default)

The scheduled heartbeat that keeps the fleet alive only as long as it behaves.

```bash
node prototypes/gitlawb-safety/fleet-cli.mjs renew [--activity .gitlawb-activity.json]
```

`--activity` maps each instance DID to its recent change summary `{changedFiles:[…], changedLines:N}`. The safety check (`src/policy.mjs`) refuses renewal if an agent touched a protected path (the safety machinery itself, workflows, CLAUDE.md), strayed outside the allowlist, or produced an oversized diff.

**Sandbox note / Phase dependency:** fetching real per-agent activity from each GitLawb node is the Phase 1 transport task (libp2p / signed HTTP) and is **not yet wired**. The policy now **fails closed** for safety-critical renewals when activity is missing, so unattended renewals will be denied with `missing_activity` until that feed exists. Call this out in the notification; do not bypass it by inventing empty activity.

Parse CLI output `RENEWED N DENIED M` plus any `denied <did> <reason>` lines. Log:
```
## gitlawb-fleet (renew)
- Verdict: [GLFLEET_OK | GLFLEET_DENIED:M]
- Renewed: N · Denied: M
- Denials: [<short_did>: <reason>, …] or "none"
```
**Notify only when** M > 0 or the fleet is empty-but-initialized changed since last run, otherwise stay silent (a healthy renew is a no-op the operator shouldn't be trained to ignore).

## Spawn Mode (`spawn <label> [node=<id>] [caps=<a,b>]`)

```bash
node prototypes/gitlawb-safety/fleet-cli.mjs spawn "<label>" --node "<id>" --caps "agent/deploy,pr/merge@repo:aeon/bot"
```
Defaults: caps `agent/deploy`, ttl 300s (clamped by the guard regardless of request). Any repo-mutating capability must be explicitly scoped as `ability@resource`; e.g. `pr/merge@repo:aeon/bot` or `git/push@repo:aeon/docs`. Parse `SPAWNED <label> <did> cap_exp=<ts>`. The CLI mirrors into `memory/instances.json`. Log + notify the new DID and expiry. **Always confirm intent in the notification** — spawning is a privilege-granting action.

## Kill Mode (`kill <did> [reason]`)

```bash
node prototypes/gitlawb-safety/fleet-cli.mjs kill "<did>" "<reason>"
```
Blocklists the DID (every token in its chain is denied at the bridge immediately) and marks it `revoked` so the renew loop never re-mints it. Parse `KILLED <did>`. Log + notify.

## List Mode (`list` / `status`)

```bash
node prototypes/gitlawb-safety/fleet-cli.mjs list
```
Each row: `<status> <label> <did>`, status ∈ `active | expiring-soon | expiring | expired | revoked`. Summarize counts. Notify a compact table (cap at 12 rows, append `…and N more`).

## Exit taxonomy

- `GLFLEET_OK` — completed normally
- `GLFLEET_DENIED:M` — renew refused M instances (cap will expire)
- `GLFLEET_NO_NODE` — node runtime missing
- `GLFLEET_NO_OPERATOR` — operator not initialized
- `GLFLEET_BAD_VAR:<var>` — unparseable command

## Constraints

- **Never commit, log, or notify the contents of `.gitlawb-vault/`.** Keys are secret.
- Never raise a safety-critical capability's TTL above the guard's ceiling — a long-lived `repo/admin` is un-recallable on a public mesh.
- The operator key and `src/policy.mjs` must stay outside any path an agent can rewrite (the policy itself enforces this; don't relax it).
- The revocation blocklist is non-authoritative on public nodes — treat it as an emergency brake, not the primary control. Expiry is the primary control.
- Don't change the skill's var semantics or the CLI contract without updating both.

Write complete, working invocations. No TODOs.
