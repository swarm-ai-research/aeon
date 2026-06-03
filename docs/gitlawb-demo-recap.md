# GitLawb Demo Recap

Ran the hardened GitLawb prototype from `pr-4` (`f58c89f0`) in an isolated worktree at `/private/tmp/aeon-pr4-demo`.

## What we ran

```bash
cd /private/tmp/aeon-pr4-demo/prototypes/gitlawb-safety
node demo.mjs
node phase2.mjs
node phase3.mjs
node phase5.mjs
```

## What it proved

### 1. Authority is short-lived by default

`demo.mjs` confirmed the capability layer behaves the way we need for GitLawb:

- never-expiring dangerous tokens are refused
- safety-critical capabilities are clamped to a 5-minute TTL
- delegation chains are verified
- privilege escalation is rejected
- renewal failure removes authority at expiry
- revocation kills authority immediately

Core takeaway: **expiry is the off-switch, renewal is the oversight hook.**

### 2. Fleet lifecycle control works

`phase2.mjs` showed the prototype is not just a token demo.

- two GitLawb-hosted Aeon instances spawned with expiring caps
- the compliant instance renewed successfully
- the unsafe instance was denied renewal for touching protected safety code
- that instance lost authority one TTL window later
- the other instance was killed immediately via blocklist
- both rows mirrored into the `fleet-control` registry shape with `host=gitlawb`

Core takeaway: **this is a credible fleet-control primitive, not just capability theory.**

### 3. Self-evolution can be gated without GitHub branch protection

`phase3.mjs` turned merge permission into a bounded capability.

- a benign change received a short-lived `pr/merge` capability
- that approval was bound to one exact diff
- reusing the approval for a different diff was blocked
- proposals touching the safety machinery were refused
- red-team refusal blocked minting
- expiry killed the merge window
- the bridge enforced the same caveat as defense-in-depth

Core takeaway: **the merge gate becomes portable instead of living in GitHub settings.**

### 4. Fleet coordination stays least-privilege

`phase5.mjs` completed the story with observability and swarm coordination.

- lifecycle events across spawn, renew, kill, review, and merge were recorded
- parallel workers got scoped, self-expiring capabilities
- hierarchical runs delegated attenuated capabilities down a verified chain
- the system emitted a dashboard-ready observability snapshot

Observed snapshot:

- Instances: `3 total (active 1 · expiring 1 · revoked 1)`
- Spawns: `3`
- Kills/revokes: `1`
- Dispatches: `4`
- Renewals: `2/3 passed (67%)`
- Authorizations: `allow 6 · deny 0`
- Merge gate: `approved 1 · denied 1 · reviews refused 1`

Core takeaway: **coordination does not require lingering authority.**

## Why this matters

Aeon already had fleet spawning, fleet monitoring, and a self-healing loop. The GitLawb prototype adds the missing decentralized control layer: scoped authority, short-lived power, gated renewal, portable merge approval, and observable coordination.

That is the real claim behind the demo: Aeon on GitLawb could support a very large autonomous fleet without giving up the operator's ability to constrain, observe, and withdraw power.

## Best one-paragraph version

Aeon on GitLawb now demos the full control loop: short-lived capabilities, renewal-gated authority, diff-bound self-evolution approval, and fleet-wide observability. In the hardened `pr-4` prototype, unsafe agents do not quietly keep power when visibility is missing or behavior drifts; they lose it. That makes the GitLawb path interesting not because it maximizes raw autonomy, but because it makes large-scale autonomy temporary, visible, and withdrawable.

## Related notes

- [[gitlawb-demo-script]] — GitLawb Demo Script _(similarity 0.60)_

<!-- suggested by scripts/suggest-edges.mjs — edit or remove freely -->
