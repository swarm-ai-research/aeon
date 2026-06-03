# gitlawb-safety (prototype)

A zero-dependency prototype of the **safety / capability-lifecycle layer** for
running Aeon agents on [GitLawb](https://github.com/Gitlawb) — the decentralized,
agent-first git platform ("no central authority").

It exists because of a specific finding: GitLawb gives you good capability
*granting* (Ed25519 + `did:key` + UCAN) but, as of v0.1, **no real enforcement
or revocation**. This prototype supplies the missing half at the trust boundary
Aeon controls.

## Why this layer is needed

Pulled directly from the GitLawb repos (`Gitlawb/node`, `Gitlawb/contracts`):

| Finding (GitLawb v0.1) | Source | What this prototype does about it |
|---|---|---|
| `exp` is optional — a token with no `exp` **never expires** (`is_expired()` returns false) | `gitlawb-core/src/ucan.rs` | `ucan.issue()` **refuses** to mint without a TTL |
| **No revocation** — "issued UCAN tokens cannot be revoked before expiry … valid for 30 days" | `node/SECURITY.md` | short mandatory TTLs + a local `RevocationStore` blocklist as emergency brake |
| **Chain not walked** — "does not yet walk the full UCAN delegation chain; any registered agent with a valid HTTP Signature can push" | `node/SECURITY.md` | `verifyChain()` walks the whole proof chain and enforces attenuation, run on every event at the bridge |
| Dangerous abilities exist as first-class caps: `agent/deploy`, `repo/admin`, `pr/merge` | `gitlawb-core/src/ucan.rs` | these are flagged `SAFETY_CRITICAL`: hard 5-min TTL ceiling + mandatory renewal-gating |
| No slashing; staking on Base **Sepolia** (testnet) | `node/docs/ECONOMICS.md`, `SECURITY.md` | out of scope for this layer — see ROADMAP Phase 4 |

The core idea: because revocation isn't available, **expiry is the only real
off-switch**. So safety-critical capabilities are minted short-lived and must be
*continuously re-earned* through a gated renewal check (e.g. a red-team
sub-swarm signing off). "Stop renewing" is the kill switch.

## Run it

```bash
node demo.mjs       # Phase 0 — capability primitives + guard
node phase1.mjs     # Phase 1 — bridge rejects forged/over-scoped/expired/revoked writes
node phase2.mjs     # Phase 2 — spawn, gated renewal, kill-switch drill
node phase3.mjs     # Phase 3 — self-evolution merge-gate as a portable capability
node phase4.mjs     # Phase 4 — economic gate: stake/heartbeat/slash node trust
node phase5.mjs     # Phase 5 — observability snapshot + swarm coordination
```

Requires Node ≥ 18 (uses built-in `crypto` Ed25519). No install step, no deps.

`demo.mjs` narrates each gap and shows the guard closing it: refusing no-expiry
tokens, clamping TTLs, rejecting privilege escalation and untrusted roots,
gating renewal, blocklisting a compromised identity, and expiry killing a token
with zero coordination.

`phase1.mjs` runs the enforcement **bridge** against a mock node: it verifies
the RFC 9421 HTTP signature, binds the request to the capability holder, and
walks the UCAN chain — forwarding one valid write while rejecting forged,
over-scoped, expired, replayed-by-the-wrong-sender, escalated, and revoked
writes. The node is never trusted to enforce any of it.

`phase2.mjs` spawns two GitLawb-hosted instances, renews them through the
safety gate (one passes, one is refused for touching the safety machinery),
then proves both off-switches: stop-renewing → dies at expiry within one TTL
window; blocklist → denied immediately.

`phase3.mjs` reviews a self-evolution proposal, mints a `pr/merge` capability
bound to that exact diff, and proves an approval can't be reused for another
diff, a self-edit of the gate is refused, a red-team flag blocks the merge, the
window expires — all with no GitHub repo. The bridge enforces the same caveat
as defense-in-depth.

## Self-evolution merge-gate (Phase 3)

Aeon's safety today is GitHub branch protection. On GitLawb there's no central
repo to protect, so "permission to merge this self-evolution" becomes a
capability: `SelfEvolutionGate.review()` runs an automated policy check then a
red-team review, and only on approval mints a short-lived `pr/merge` UCAN
**bound by a caveat to the hash of that exact diff**. `authorizeMerge()` (and
the bridge, for `pr-merge` events) allows a merge only when the cap's caveat
matches the change. This is what a GitLawb v0.2 node enforces server-side; the
bridge runs it today, unchanged when it migrates node-side.

## Economic node trust (Phase 4)

`NodeTrustPolicy` is the bridge's outermost gate: it accepts events only from
nodes that are registered, staked above the minimum (10k $GITLAWB), heartbeating
within 3 days, and not slashed — reading from a `StakeOracle`. The relaying
node's id is **authenticated**: it signs the request it relays with its own key
(`did:key`), so an unstaked node can't claim a staked node's id to pass the
gate. This makes a rogue relay cost real capital — the Sybil floor the
merge-gate and off-switch assume. The oracle is an interface:
`BaseChainStakeOracle` reads `GitlawbNodeStaking`/`GitlawbStaking` on Base once
mainnet + slashing are live (`refresh()` caches it; `nodeStatus()` stays
synchronous for the per-event hot path); `MockStakeOracle` stands in today
(GitLawb v1 has no slashing and staking is paused on Sepolia). Only the oracle
changes when the data goes real.

## Observability + coordination (Phase 5)

Every safety decision (spawn, renew, kill, authorize, review, merge, dispatch)
is emitted into a `MetricsRecorder`; `aggregate()` rolls a window into a
snapshot and `snapshotToMarkdown()` renders it for `./notify` → the dashboard.
The `gitlawb-fleet-metrics` skill emits it daily:

```bash
node fleet-cli.mjs metrics --hours 24   # dashboard-ready markdown snapshot
```

`SwarmCoordinator` steers the fleet on top of the capability layer:
`runParallel` mints a scoped, short-lived cap per worker; `runHierarchical`
mints to a lead that delegates attenuated caps to its children (the chain the
bridge verifies). Coordinated authority is least-privilege and self-expiring —
a run leaves no lingering grants.

## The bridge (Phase 1)

Because GitLawb v0.1 doesn't walk the delegation chain ("any registered agent
with a valid HTTP Signature can push"), the bridge re-checks **every** write
event before Aeon acts on it: (1) RFC 9421 signature valid, (2) sender == token
audience, (3) UCAN chain authorizes the required capability (walk + attenuate +
revocation). Run it as a service:

```bash
node bridge-cli.mjs run --events events.json   # replay/audit a batch of events
```

The production event source is `GossipEventSource` (libp2p) — a Phase 1 infra
task that can't run in this sandbox; without `--events` the CLI says so. Front
your GitLawb node privately so the bridge is the only ingress — see
`node.env.example` (`GITLAWB_PUBLIC_READ=false`, don't expose
`git-receive-pack`).

## Use it as a fleet (CLI + Aeon skill)

```bash
node fleet-cli.mjs init                 # create the operator root identity
node fleet-cli.mjs spawn aeon-alpha     # mint a 5-min agent/deploy + pr/merge
node fleet-cli.mjs renew                # gated re-mint of every live instance
node fleet-cli.mjs kill <did> reason    # blocklist + stop renewing
node fleet-cli.mjs list                 # effective status per instance
```

The `gitlawb-fleet` skill (`skills/gitlawb-fleet/SKILL.md`) wraps this for Aeon:
empty `var` runs the renewal loop on a schedule, `spawn`/`kill`/`list` are
var-driven. Private keys live in a gitignored vault (`.gitlawb-vault/`); the
public registry (`memory/gitlawb-fleet.json`) is mirrored into
`memory/instances.json` so `fleet-control` sees GitLawb instances too.

## Task runner (prototype)

The capability layer and task queue are not enough by themselves: assigned
tasks remain idle until a runner polls the node, claims work, executes it, and
reports the result back. The prototype runner does exactly that:

```bash
cp memory/gitlawb-runner.example.json memory/gitlawb-runner.json
node task-runner.mjs once
node task-runner.mjs loop --poll 30
```

What it does:

- reads GitLawb-hosted agents from `memory/instances.json`
- polls `gl task list --status pending --assignee-did <did>`
- claims each task with the agent's `identity_dir`
- runs either a configured shell hook or a built-in prototype executor
- supports `executor: "autonomous"` for Codex/Claude-in-the-loop executors:
  the runner repeats the executor, passes each step JSON to a configured
  `harnessCommand`, feeds the reported action back through
  `GITLAWB_LAST_ACTION_JSON`, and stops on completion, doom-loop, or `maxSteps`
- writes a full artifact to `memory/gitlawb-runner/<task-id>.json`
- completes or fails the task on the node
- keeps GitLawb proof writes pinned to the configured repo + branch instead of trusting per-task overrides
- contains claim failures to the individual task so one race or malformed task does not abort the full pass

Offline / sandboxed testing:

```bash
node task-runner.mjs once --tasks-file /tmp/tasks.json --dry-run
node task-runner.test.mjs
```

The built-in executors are intentionally lightweight: research, review,
deployment prep, and security audit summaries for the current repo. For real
work, replace them per agent in `memory/gitlawb-runner.json` with command hooks
that run your preferred local executor.

Autonomous executors need a local harness command that can read the step prompt
from stdin, execute one action, and return JSON: `{ "type": "action", ... }`,
`{ "type": "complete", ... }`, or `{ "type": "fail", ... }`. In GitHub Actions
the example researcher config uses the `claude` CLI with subscription auth via
`CLAUDE_CODE_OAUTH_TOKEN`; no `ANTHROPIC_API_KEY` is passed to the runner step.

For write-capable prototype executors, set `repoUrl` and `branch` in
`memory/gitlawb-runner.json`. Task payloads may request proof work, but they
cannot redirect the runner to a different repo or ref.
## Layout

```
src/identity.mjs    Ed25519 keypairs + did:key encode/decode (real crypto)
src/caps.mjs        capability vocabulary + safety-critical set + TTL ceilings
src/ucan.mjs        UCAN-shaped tokens: issue / delegate / verify / verifyChain
src/revocation.mjs  local DID + token blocklist (the emergency brake)
src/guard.mjs       CapabilityGuard — the bridge / off-switch
src/store.mjs       FleetStore — public registry + gitignored key vault
src/policy.mjs      automated renewal safety check (red-team plugs in here)
src/fleet.mjs       GitLawbFleet — spawn / renewAll / kill / mirror (Phase 2)
src/httpsig.mjs     RFC 9421 HTTP Message Signatures over Ed25519 (Phase 1)
src/transport.mjs   event sources: MockEventSource + GossipEventSource skeleton
src/bridge.mjs      Bridge — the long-running enforcement service (Phase 1/3)
src/evolution.mjs   SelfEvolutionGate — per-diff merge capability (Phase 3)
src/stake.mjs       StakeOracle + NodeTrustPolicy — economic node trust (Phase 4)
src/metrics.mjs     MetricsRecorder + aggregate + snapshot markdown (Phase 5)
src/coordinator.mjs SwarmCoordinator — parallel/hierarchical dispatch (Phase 5)
fleet-cli.mjs       CLI used by the gitlawb-fleet skill (+ metrics subcommand)
task-runner.mjs     polls GitLawb tasks, claims them, runs agent executors
bridge-cli.mjs      run the bridge as a service
demo.mjs            Phase 0 scenario
phase1.mjs          Phase 1 bridge enforcement
phase2.mjs          Phase 2 spawn + kill-switch drill
phase3.mjs          Phase 3 self-evolution merge-gate
phase4.mjs          Phase 4 economic node-trust gate
phase5.mjs          Phase 5 observability + coordination
node.env.example    how to run the GitLawb node private behind the bridge
```

## Scope / honesty

This is a **prototype of the control logic**, not production infrastructure.
What it deliberately models faithfully: the UCAN shape, `did:key` encoding,
real Ed25519 signing/verification, attenuated proof chains. What it stubs:
transport (no libp2p), persistence (in-memory store), and the safety check
itself (a pluggable async function, not a real red-team swarm). See
`ROADMAP.md` for how this becomes a real integration and what each step depends
on from GitLawb's own maturity.
