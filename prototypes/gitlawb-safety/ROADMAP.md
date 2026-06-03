# Roadmap — Aeon on GitLawb

Integrating Aeon (autonomous agent on GitHub Actions) with GitLawb (decentralized,
agent-first git; "no central authority") so Aeon can spawn and coordinate a fleet
on a decentralized substrate — **without losing the oversight that GitHub's
centralization gives Aeon today.**

## The governing constraint

Aeon's safety today *is* GitHub's centralization: branch protection, required
checks, merge gates. GitLawb deliberately removes the central authority those
depend on. So the whole roadmap is organized around one question:

> Where does the merge-gate / off-switch live when there is no central repo to protect?

Answer this layer commits to: **short-lived capabilities + gated renewal**, because
GitLawb has no revocation. Expiry is the off-switch; renewal is the oversight hook.

## GitLawb maturity gates (what blocks what)

Several phases can't be trusted until GitLawb itself matures. Tracked explicitly:

| Capability we need | GitLawb status (v0.1) | Unblocks |
|---|---|---|
| UCAN issuance / delegation / `did:key` | ✅ shipped (`gitlawb-core`) | Phase 1 |
| Server-side delegation-chain enforcement | ❌ v0.1 doesn't walk the chain; "any signed agent can push" | Phase 3 |
| Token revocation | ❌ none; 30-day compromise window | (never — we design around it) |
| Authenticated `git-receive-pack` over plain HTTP | ❌ unauthenticated unless via `gitlawb://` helper | Phase 1 (run private) |
| On-chain staking / Sybil cost | ⚠️ Base **Sepolia** testnet, no slashing in v1 | Phase 4 |

**Strategy: don't wait on GitLawb.** Phases 1–2 put all enforcement on *our* side
(bridge + guard) and treat the node as untrusted. We only migrate enforcement
onto GitLawb (Phase 3+) once its server-side checks ship.

---

## Phase 0 — Spike *(this prototype, done)*

- **Deliverable:** runnable capability-lifecycle core — mandatory TTLs,
  `verifyChain` attenuation, gated renewal, local blocklist. See `README.md`.
- **Exit:** the control logic is demonstrably correct in isolation. ✅

## Phase 1 — Bridge-side enforcement *(works against GitLawb v0.1 today)* ✅ *(prototype done)*

Treat every GitLawb node as untrusted; enforce capabilities ourselves.

- **Built:**
  - `Bridge` (`src/bridge.mjs`) — the enforcement service. On every event:
    (1) verify the RFC 9421 HTTP signature (`src/httpsig.mjs`), (2) bind sender
    == signature keyid == token audience, (3) `guard.authorize()` (walk chain +
    attenuate + revocation). Only all-pass events are forwarded.
  - `src/transport.mjs` — `MockEventSource` (fully testable) + `GossipEventSource`
    skeleton documenting the libp2p infra dependency. `bridge-cli.mjs` runs it.
  - `createBridgeFromStore` shares the operator root + the SAME revocation store
    `gitlawb-fleet kill` writes to → a kill propagates to bridge decisions with
    no extra plumbing. Revocation store is file-backed (survives restart);
    Postgres/SQLite swaps in behind the same interface.
  - `node.env.example` — run the node private (`GITLAWB_PUBLIC_READ=false`,
    don't expose `git-receive-pack`), making the bridge the only ingress.
  - **Merge-gate stays on the GitHub side** in this phase, as planned.
  - **Exit criterion met** — `node phase1.mjs`: 1 valid write forwarded; forged,
    over-scoped, expired, stolen-token, escalated, and revoked writes all
    rejected at the bridge, with the node trusted for nothing.
- **Still stubbed:** the libp2p `GossipEventSource` (needs a host + bootstrap
  peers; can't run in-sandbox). Until it's wired, the bridge replays events via
  `--events`. This is the same transport task Phase 2's live activity feed needs.

## Phase 2 — Spawn + lifecycle *(Aeon fleet on GitLawb)* ✅ *(prototype done)*

Wire the off-switch to real spawning, reusing Aeon's existing fleet machinery.

- **Built:**
  - `GitLawbFleet.spawn()` (`src/fleet.mjs`) — mints a 5-min `agent/deploy`
    (+ `pr/merge`) via the guard for a fresh identity; private key to a
    gitignored vault (`src/store.mjs`), public record to `memory/gitlawb-fleet.json`.
  - **Renewal loop** — `GitLawbFleet.renewAll()` re-mints each live agent's caps
    only after `safetyCheck()` passes. Default automated check (`src/policy.mjs`):
    diff-size cap, touched-paths allowlist, and a hard block on rewriting the
    safety machinery itself. The interface a red-team sub-swarm plugs into later.
  - "Spawn a clone" → short-lived `agent/deploy`; "self-evolution PR merge" →
    short-lived `pr/merge`, both issued only post-check.
  - Mirrored into `memory/instances.json` (`syncToInstancesRegistry`) with
    `host: "gitlawb"`; `fleet-control` made host-aware so it reports them
    without `gh`. Driven by the `gitlawb-fleet` skill + `fleet-cli.mjs`.
  - **Exit criterion met** — `node phase2.mjs` shows both stops: failed gate →
    capability dies at expiry (`link:expired`) within one TTL window; blocklist
    → denied immediately (`revoked`). No central repo involved.
- **Still stubbed (Phase 1 transport dependency):** per-agent activity is fed in
  manually (`--activity`); fetching it from each GitLawb node over libp2p/signed
  HTTP is Phase 1. Until then, unattended renewal is provisional.

## Phase 3 — Migrate the gate onto GitLawb *(gate built; full migration awaits GitLawb v0.2)* ✅ *(prototype done)*

Model the self-evolution merge-gate as a capability instead of a GitHub setting.

- **Built:**
  - `SelfEvolutionGate` (`src/evolution.mjs`) — `review(proposal)` runs the
    automated policy check, then a pluggable red-team review (a sub-swarm in
    production); only on approval does it mint a short-lived `pr/merge` UCAN
    **bound by a caveat to the hash of that exact diff** (`proposalHash`).
  - `authorizeMerge()` allows a merge only if the presented cap's caveat matches
    the change being merged — an approval for one diff cannot merge another.
  - **Defense-in-depth wired into the bridge:** `pr-merge` events carry the
    proposal inside the signed body; the bridge enforces the caveat
    (`enforceMergeCaveat`). This is exactly what a GitLawb v0.2 node enforces
    server-side once it walks the chain — same code, just relocated.
  - **Exit criterion met** — `node phase3.mjs`: an approved change merges; reuse
    of the approval for a different diff, a self-edit of the gate, a red-team
    flag, an expired window, and a bridge-side swapped diff are all blocked,
    with **no GitHub repo involved**. The gate is portable across nodes.
- **Still awaits GitLawb v0.2:** moving `authorizeMerge` enforcement from our
  bridge onto the node itself (server-side chain validation). Until then the
  bridge is the enforcement point; the logic doesn't change when it migrates.

## Phase 4 — Economic / Sybil hardening *(consumer side built; live data awaits GitLawb mainnet)* ✅ *(prototype done)*

- **Depends on:** GitLawb staking on mainnet + a slashing mechanism (v1 has
  neither; staking is paused on Base Sepolia testnet). So the on-chain numbers
  aren't economically real yet — but the bridge-side policy that consumes them
  is buildable now.
- **Built:**
  - `StakeOracle` interface (`src/stake.mjs`): `BaseChainStakeOracle` is the
    skeleton that reads `GitlawbNodeStaking` / `GitlawbStaking` on Base once
    live; `MockStakeOracle` stands in until then. Tier table + node minimums
    come straight from `docs/ECONOMICS.md`.
  - `NodeTrustPolicy` — the bridge's economic gate: rejects events relayed by
    nodes that are unregistered, under-staked (< 10k $GITLAWB), stale
    (heartbeat > 3 days), or slashed. Wired as the outermost `Bridge` check.
  - **Exit criterion met** — `node phase4.mjs`: the same valid, signed,
    properly-capability'd write is accepted from a staked/live node and rejected
    from under-staked / stale / slashed / unregistered nodes. Being trusted
    costs real capital; misbehavior (once slashing ships) burns it.
- **Still awaits GitLawb mainnet:** swapping `MockStakeOracle` →
  `BaseChainStakeOracle`. The bridge logic doesn't change — only the oracle.

## Phase 5 — Observability + coordination *(scale-out)* ✅ *(prototype done)*

- **Built:**
  - `MetricsRecorder` + `aggregate` + `snapshotToMarkdown` (`src/metrics.mjs`):
    every safety decision (spawn, renew, kill, authorize, review, merge,
    dispatch) is emitted as an event; rolled into a windowed snapshot. Optional
    everywhere — components without a recorder behave unchanged.
  - `fleet-cli.mjs metrics` + the `gitlawb-fleet-metrics` skill emit a daily
    dashboard card via `./notify` (renders through notify-jsonrender).
  - `SwarmCoordinator` (`src/coordinator.mjs`): `runParallel` and
    `runHierarchical` dispatch sub-tasks with freshly-minted, scoped,
    short-lived caps (children get attenuated delegations off the lead) — so
    coordinated authority is least-privilege and self-expiring.
  - **Exit criterion met** — `node phase5.mjs`: a multi-agent fleet is
    observable (snapshot: instance health, renewal pass-rate, kills, merge-gate)
    and steerable (parallel + hierarchical runs over verified capability chains).

---

## Risk register (carry forward)

1. **No revocation is permanent design pressure.** Never mint a safety-critical
   cap with a long TTL "for convenience" — a leaked long-lived `repo/admin` is
   un-recallable on a public mesh. Enforce the ceiling in the minting layer.
2. **The blocklist is non-authoritative on public nodes.** It only protects
   actions that flow through our bridge. Treat it as an emergency brake, not the
   primary control.
3. **v0.1 plain-HTTP push is unauthenticated.** Until fixed, never expose the
   node's `git-receive-pack` publicly.
4. **Testnet economics ≠ Sybil resistance.** Don't assume stake-based trust
   until Phase 4's dependency lands on mainnet with slashing.
5. **Self-evolution must not be able to evolve away its own gate.** The renewal
   check and trusted-root set must live outside any repo an agent can rewrite.
