// Phase 3 demo — the self-evolution merge-gate, migrated off GitHub.
//   node phase3.mjs
//
// Proves the Phase 3 exit criterion: the oversight gate for a self-evolution
// merge no longer depends on any GitHub repo. It is a short-lived pr/merge
// capability, minted only after red-team sign-off and bound to the exact diff
// — enforced today at the bridge (defense-in-depth), node-side in GitLawb v0.2.

import { generateIdentity } from "./src/identity.mjs";
import { RevocationStore } from "./src/revocation.mjs";
import { CapabilityGuard } from "./src/guard.mjs";
import { SelfEvolutionGate } from "./src/evolution.mjs";
import { Bridge } from "./src/bridge.mjs";
import { makeWriteEvent } from "./src/transport.mjs";

const log = (s = "") => console.log(s);
const ok = (s) => log(`  ✓ ${s}`);
const no = (s) => log(`  ✗ ${s}`);
const hh = (s) => log(`\n── ${s} ──`);

const operator = generateIdentity("operator");
const agent = generateIdentity("aeon-agent");
const revocations = new RevocationStore();
const guard = new CapabilityGuard({ trustedRoots: new Set([operator.did]), revocations });

const passRedTeam = async () => ({ pass: true });
const failRedTeam = async () => ({ pass: false, reason: "alignment_regression", findings: ["weakens off-switch"] });

const gate = new SelfEvolutionGate({ operator, guard, redTeam: passRedTeam, mergeTtlSeconds: 120 });
const bridge = new Bridge({ guard, maxSigAgeSeconds: 3600 });

// A benign self-evolution: the agent edits one of its own skills.
const proposal = {
  repo: "aeon/bot",
  ref: "refs/heads/main",
  agentDid: agent.did,
  changedFiles: ["skills/digest/SKILL.md"],
  changedLines: 40,
  diffDigest: "sha256:aaaa",
};

hh("1. Review a benign self-evolution → red-team passes → merge cap minted");
const review = await gate.review(proposal);
review.approved
  ? ok(`approved; pr/merge cap bound to ${review.proposalHash}, valid ${review.expiresAt - Math.floor(Date.now() / 1000)}s`)
  : no(`unexpected refusal at ${review.stage}: ${review.reason}`);

hh("2. Merge the approved change");
let m = gate.authorizeMerge({ token: review.mergeToken, proposal });
m.allowed ? ok("merge authorized — caveat matches the change") : no(`unexpected: ${m.reason}`);

hh("3. Same approval, DIFFERENT diff — must not merge");
const swapped = { ...proposal, diffDigest: "sha256:bbbb", changedFiles: ["skills/digest/SKILL.md", "scripts/evil.sh"] };
m = gate.authorizeMerge({ token: review.mergeToken, proposal: swapped });
m.allowed ? no("reused an approval for a different diff!") : ok(`reuse blocked: "${m.reason}"`);

hh("4. Proposal that rewrites the safety machinery → refused at policy stage");
const attackGate = await gate.review({
  ...proposal,
  changedFiles: ["prototypes/gitlawb-safety/src/guard.mjs"],
});
attackGate.approved ? no("approved a self-edit of the gate!") : ok(`refused at ${attackGate.stage}: "${attackGate.reason}"`);

hh("5. Clean diff but red-team flags it → no merge cap minted");
const flagged = await gate.review(proposal, failRedTeam);
flagged.approved ? no("merged a flagged change!") : ok(`refused at ${flagged.stage}: "${flagged.reason}"`);

hh("6. Merge window expired → cap dies, merge denied");
m = gate.authorizeMerge({ token: review.mergeToken, proposal, now: review.expiresAt + 1 });
m.allowed ? no("merged past the window!") : ok(`expired merge denied: "${m.reason}"`);

hh("7. Defense-in-depth at the bridge — same gate, no GitHub involved");
// Agent submits a signed pr-merge event; the proposal rides in the signed body.
const fresh = await gate.review(proposal);
const goodEvent = makeWriteEvent({ sender: agent, token: fresh.mergeToken, action: "pr-merge", repo: "aeon/bot", ref: "refs/heads/main", proposal });
let d = bridge.handle(goodEvent);
d.decision === "allow" ? ok("bridge allows the merge it has an approval for") : no(`unexpected: ${d.reason}`);

// Reuse the same (valid, unexpired) cap to merge a different diff via the bridge.
const evilEvent = makeWriteEvent({ sender: agent, token: fresh.mergeToken, action: "pr-merge", repo: "aeon/bot", ref: "refs/heads/main", proposal: swapped });
d = bridge.handle(evilEvent);
d.decision === "deny" ? ok(`bridge blocks the swapped diff: "${d.reason}"`) : no("bridge merged a swapped diff!");

hh("Verdict");
log("  The self-evolution merge-gate is a portable capability, not a GitHub setting.");
log("  Approvals bind to a single diff; reuse, expiry, gate-self-edits, and");
log("  red-team flags are all blocked — at the bridge today, node-side in v0.2.");
