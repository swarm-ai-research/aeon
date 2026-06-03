// Phase 4 demo — economic trust: which nodes the bridge will accept from.
//   node phase4.mjs
//
// Exit criterion: being a trusted node costs real capital. The SAME valid,
// signed, properly-capability'd write is accepted when relayed by a staked,
// live, unslashed node — and rejected when the relaying node is unregistered,
// under-staked, stale, or slashed.
//
// NOTE: the stake data is mocked. GitLawb v1 has no slashing and staking is
// paused on Base Sepolia (testnet), so there is nothing real to read yet; the
// MockStakeOracle stands in for BaseChainStakeOracle. The bridge logic is
// final — only the oracle changes when mainnet + slashing land.

import { generateIdentity } from "./src/identity.mjs";
import { cap, CAP } from "./src/caps.mjs";
import { RevocationStore } from "./src/revocation.mjs";
import { CapabilityGuard } from "./src/guard.mjs";
import { Bridge } from "./src/bridge.mjs";
import { makeWriteEvent } from "./src/transport.mjs";
import { MockStakeOracle, NodeTrustPolicy } from "./src/stake.mjs";

const log = (s = "") => console.log(s);
const hh = (s) => log(`\n── ${s} ──`);

const now = Math.floor(Date.now() / 1000);
const DAY = 24 * 3600;

const operator = generateIdentity("operator");
const agent = generateIdentity("aeon-agent");
const revocations = new RevocationStore();
const guard = new CapabilityGuard({ trustedRoots: new Set([operator.did]), revocations });

// Each node has its OWN keypair; its did:key is what stake is registered
// against. The relay must sign with that key — it can't just claim a did.
const nodes = {
  validator: generateIdentity("node-validator"),
  curator: generateIdentity("node-curator"),
  thin: generateIdentity("node-thin"),
  stale: generateIdentity("node-stale"),
  slashed: generateIdentity("node-slashed"),
  rogue: generateIdentity("node-rogue"), // has a key, but no stake registered
};

// On-chain standing keyed by node did (amounts in $GITLAWB). node-rogue absent.
const oracle = new MockStakeOracle({
  [nodes.validator.did]: { staked: 1_000_000, lastHeartbeat: now - 3600, slashed: false },
  [nodes.curator.did]: { staked: 10_000, lastHeartbeat: now - 7200, slashed: false },
  [nodes.thin.did]: { staked: 5_000, lastHeartbeat: now - 3600, slashed: false },
  [nodes.stale.did]: { staked: 1_000_000, lastHeartbeat: now - 5 * DAY, slashed: false },
  [nodes.slashed.did]: { staked: 1_000_000, lastHeartbeat: now - 3600, slashed: true },
});
const nodeTrust = new NodeTrustPolicy({ oracle });
const bridge = new Bridge({ guard, nodeTrust, maxSigAgeSeconds: 3600 });

// One agent, one legitimate capability. The ONLY thing that varies below is
// which node relays the (identical, valid) write.
const token = guard.mint({
  issuer: operator,
  audienceDid: agent.did,
  capabilities: [cap("repo:aeon/bot", CAP.GIT_PUSH)],
  ttlSeconds: 300,
});

function relayFrom(label, nodeIdentity) {
  const event = makeWriteEvent({ sender: agent, token, action: "push", repo: "aeon/bot", ref: "refs/heads/main", nodeIdentity });
  const d = bridge.handle(event, { now });
  const nt = nodeIdentity ? nodeTrust.evaluate(nodeIdentity.did, { now }) : {};
  const suffix = d.decision === "allow" ? `(tier=${nt.tier}, stake=${nt.stake})` : `"${d.reason}"`;
  log(`  [${d.decision === "allow" ? "ALLOW" : "DENY "}] relayed by ${label.padEnd(14)} ${suffix}`);
}

hh("Same valid write, different relaying node");
relayFrom("node-validator", nodes.validator); // staked 1M, live → trusted
relayFrom("node-curator", nodes.curator); //    staked 10k (== min), live → trusted
relayFrom("node-thin", nodes.thin); //          staked 5k (< 10k min) → rejected
relayFrom("node-stale", nodes.stale); //        staked 1M but heartbeat 5d old → rejected
relayFrom("node-slashed", nodes.slashed); //    staked 1M but slashed → rejected
relayFrom("node-rogue", nodes.rogue); //        has a key, no stake → rejected

hh("Impersonation — attacker claims a staked node's did but lacks its key");
const forged = makeWriteEvent({ sender: agent, token, action: "push", repo: "aeon/bot", ref: "refs/heads/main", nodeIdentity: nodes.rogue });
forged.node = nodes.validator.did; // claim the validator's id, keep rogue's signature
const d = bridge.handle(forged, { now });
log(`  [${d.decision === "allow" ? "ALLOW" : "DENY "}] relayed by ${"impersonator".padEnd(14)} "${d.reason}"`);

hh("Verdict");
log("  A node must stake ≥10k $GITLAWB, keep a live heartbeat, and PROVE its id");
log("  by signing what it relays. A slash (once GitLawb ships it) revokes trust.");
log("  Claiming a staked id without its key fails; spinning up a real staked node");
log("  costs capital — the Sybil floor the merge-gate and off-switch assume.");
log("\n  (stake data mocked — BaseChainStakeOracle reads this on Base once live)");
