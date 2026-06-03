# GitLawb Demo Script

This is the shortest live walkthrough that shows why Aeon on GitLawb matters.

Use the hardened prototype branch in an isolated worktree:

```bash
git worktree add /private/tmp/aeon-pr4-demo pr-4
cd /private/tmp/aeon-pr4-demo/prototypes/gitlawb-safety
```

## Demo goal

Show four things, in order:

1. Authority is short-lived and scoped.
2. Renewal is the real off-switch.
3. Self-evolution can be gated without GitHub branch protection.
4. A fleet of agents can be coordinated and observed without leaving dangerous long-lived permissions behind.

## Run order

```bash
node demo.mjs
node phase2.mjs
node phase3.mjs
node phase5.mjs
```

Skip `phase1.mjs` in the main walkthrough unless the audience specifically wants bridge-level enforcement detail. It is good, but it slows the story down.

## 1. `node demo.mjs`

### What to say

"GitLawb gives us agent-native capabilities, but the missing piece is enforcement and revocation. This prototype rebuilds the safety layer on Aeon's side. The rule is simple: dangerous capabilities are short-lived, and agents only keep them by continuously re-earning them."

### What to point at

- No-expiry token minting is refused.
- Dangerous capabilities get clamped to a 5-minute TTL.
- Escalation and untrusted roots are rejected.
- Renewal can be denied by the safety gate.
- Revocation and expiry both kill authority.

### One-line takeaway

"Expiry is the off-switch, renewal is the oversight hook."

## 2. `node phase2.mjs`

### What to say

"Now we turn the capability model into fleet control. Aeon spawns two GitLawb-hosted instances, tries to renew both, and proves both shutdown paths."

### What to point at

- Two instances are spawned with expiring caps.
- One instance renews.
- The other is denied renewal for touching protected safety code.
- The denied instance loses capability one TTL window later.
- The other can be killed immediately via blocklist.
- The registry mirrors into `instances.json`, so fleet tooling can see GitLawb-hosted rows too.

### One-line takeaway

"This is the move from single-agent autonomy to managed population autonomy."

## 3. `node phase3.mjs`

### What to say

"GitHub branch protection is doing a lot of hidden safety work for Aeon today. On GitLawb, merge permission has to become a capability too."

### What to point at

- A benign self-evolution gets a short-lived merge capability.
- That approval is bound to one exact diff.
- Reusing the approval for another diff fails.
- Editing the safety machinery fails at policy stage.
- Red-team refusal blocks minting.
- Expiry kills the merge window.

### One-line takeaway

"The merge gate becomes portable. It's no longer a GitHub setting."

## 4. `node phase5.mjs`

### What to say

"Once the capability layer exists, the next question is whether a fleet can operate at scale without accumulating messy long-lived power. This phase shows the answer."

### What to point at

- Fleet events are recorded as a safety/operations stream.
- Parallel runs mint scoped caps per worker.
- Hierarchical runs delegate attenuated caps down a verified chain.
- The output snapshot is already shaped like a dashboard/notify card.

### One-line takeaway

"Coordination is least-privilege and self-expiring."

## Optional appendix: `node phase1.mjs`

Use this if the audience wants the enforcement layer.

### What to say

"GitLawb v0.1 does not fully enforce delegation chains server-side, so the bridge re-checks every write before Aeon acts on it."

### What to point at

- Valid writes are forwarded.
- Over-scoped writes are denied.
- Forged requests are denied.
- Stolen tokens are denied.
- Expired and revoked chains are denied.

### One-line takeaway

"The node is not trusted; the bridge is the enforcement point."

## Suggested 5-minute talk track

### Minute 1

"Aeon already knows how to spawn instances, monitor them, and repair itself. The GitLawb work matters because it gives that fleet a decentralized substrate without giving up the off-switch."

### Minute 2

Run `demo.mjs`.

"The core idea is that authority expires by default. Dangerous capabilities are short-lived, renewal is gated, and failure to renew is itself a safety mechanism."

### Minute 3

Run `phase2.mjs`.

"Now make it concrete: two agents, one safe, one not. The safe one renews. The unsafe one loses authority automatically. That is the fleet control primitive."

### Minute 4

Run `phase3.mjs`.

"The next problem is self-modification. On GitLawb, merge permission has to be granted as a bounded capability tied to one exact proposed change."

### Minute 5

Run `phase5.mjs`.

"Once you can scope, renew, revoke, and observe authority like this, you can coordinate a much larger fleet without leaving long-lived permissions lying around."

## Good closing line

"Most agent systems scale by becoming harder to stop. This one scales by making authority more temporary, more visible, and easier to withdraw."
