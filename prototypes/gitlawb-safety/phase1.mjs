// Phase 1 demo — bridge-side enforcement against an untrusted node.
//   node phase1.mjs
//
// Proves the Phase 1 exit criterion: a valid write is forwarded, and forged /
// over-scoped / expired / replayed / escalated / revoked writes are all
// rejected at the bridge — without trusting the node to reject anything.

import { mkdtempSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";

import { generateIdentity } from "./src/identity.mjs";
import { cap, CAP } from "./src/caps.mjs";
import { delegate, serializeToken, nowSec } from "./src/ucan.mjs";
import { RevocationStore } from "./src/revocation.mjs";
import { FleetStore } from "./src/store.mjs";
import { GitLawbFleet } from "./src/fleet.mjs";
import { CapabilityGuard } from "./src/guard.mjs";
import { Bridge } from "./src/bridge.mjs";
import { makeWriteEvent } from "./src/transport.mjs";

const log = (s = "") => console.log(s);
const row = (d) => {
  const mark = d.decision === "allow" ? "ALLOW" : "DENY ";
  log(`  [${mark}] ${d.action.padEnd(8)} ${(d.repo ?? "").padEnd(11)} ${d.reason ?? "ok"}`);
};
const hh = (s) => log(`\n── ${s} ──`);

const dir = mkdtempSync(join(tmpdir(), "gitlawb-bridge-"));
const store = new FleetStore({
  registryPath: join(dir, "fleet.json"),
  vaultPath: join(dir, "vault.json"),
});
const revocations = new RevocationStore(join(dir, "revocations.json"));

const operator = generateIdentity("operator");
const trustedRoots = new Set([operator.did]);
const fleet = new GitLawbFleet({ trustedRoots, store, revocations });
const guard = new CapabilityGuard({ trustedRoots, revocations });
const bridge = new Bridge({ guard, maxSigAgeSeconds: 3600 });

// Spawn alpha with push rights on exactly one repo (plus deploy).
const alpha = fleet.spawn({
  operator,
  label: "aeon-alpha",
  node: "node-1",
  capabilities: [cap("*", CAP.AGENT_DEPLOY), cap("repo:aeon/bot", CAP.GIT_PUSH)],
  ttlSeconds: 300,
});

log(`operator: ${operator.did.slice(0, 28)}…`);
log(`alpha   : ${alpha.identity.did.slice(0, 28)}…  (git/push@repo:aeon/bot)`);

hh("1. Valid write — alpha pushes to the repo it was granted");
row(bridge.handle(makeWriteEvent({
  sender: alpha.identity, token: alpha.token, action: "push", repo: "aeon/bot", ref: "refs/heads/main",
})));

hh("2. Over-scoped — alpha pushes to a repo it has no cap for");
row(bridge.handle(makeWriteEvent({
  sender: alpha.identity, token: alpha.token, action: "push", repo: "aeon/secret", ref: "refs/heads/main",
})));

hh("3. Privilege escalation — alpha delegates a cap it doesn't hold");
// alpha holds push + deploy, NOT pr/merge — so this delegation is invalid.
const subtask = generateIdentity("subtask");
const escalated = delegate({
  issuer: alpha.identity, audienceDid: subtask.did,
  capabilities: [cap("repo:aeon/bot", CAP.PR_MERGE)], ttlSeconds: 120, proof: alpha.token,
});
row(bridge.handle(makeWriteEvent({
  sender: subtask, token: escalated, action: "pr-merge", repo: "aeon/bot", ref: "refs/heads/main",
})));

hh("4. Forged request — tamper the body after signing");
const tampered = makeWriteEvent({
  sender: alpha.identity, token: alpha.token, action: "push", repo: "aeon/bot", ref: "refs/heads/main",
});
tampered.request.body += '{"sneaky":true}';
row(bridge.handle(tampered));

hh("5. Stolen token — bob signs with his own key but presents alpha's token");
const bob = generateIdentity("bob");
row(bridge.handle(makeWriteEvent({
  sender: bob, token: alpha.token, action: "push", repo: "aeon/bot", ref: "refs/heads/main",
})));

hh("6. Expired — alpha's valid write, evaluated one TTL window later");
row(bridge.handle(
  makeWriteEvent({ sender: alpha.identity, token: alpha.token, action: "push", repo: "aeon/bot", ref: "refs/heads/main" }),
  { now: alpha.token.payload.exp + 1 },
));

hh("7. Revoked — operator blocklists alpha, then alpha pushes");
fleet.kill(alpha.identity.did, "anomaly_detected");
row(bridge.handle(makeWriteEvent({
  sender: alpha.identity, token: alpha.token, action: "push", repo: "aeon/bot", ref: "refs/heads/main",
})));

hh("8. Cascading revocation — revoke a PARENT token, child is denied too");
const worker = fleet.spawn({
  operator, label: "aeon-worker", node: "node-3",
  capabilities: [cap("repo:aeon/docs", CAP.GIT_PUSH)], ttlSeconds: 300,
});
const helper = generateIdentity("helper");
const delegated = delegate({
  issuer: worker.identity, audienceDid: helper.did,
  capabilities: [cap("repo:aeon/docs", CAP.GIT_PUSH)], ttlSeconds: 120, proof: worker.token,
});
const childPush = () => makeWriteEvent({ sender: helper, token: delegated, action: "push", repo: "aeon/docs", ref: "refs/heads/main" });
row(bridge.handle(childPush())); // allowed: legit delegation
revocations.revokeToken(worker.entry.cap_token_id, "parent token compromised");
row(bridge.handle(childPush())); // denied: ancestor token revoked

hh("Verdict");
log("  2 valid writes forwarded; 7 bad/blocked writes rejected at the bridge.");
log("  The node was never trusted to enforce any of this.");
log(`\n  (state written under ${dir})`);
