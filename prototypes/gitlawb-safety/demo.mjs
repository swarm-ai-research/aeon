// Runnable end-to-end demo of the Aeon<->GitLawb safety layer.
//   node demo.mjs
//
// It walks the exact gaps found in the GitLawb v0.1 source/docs and shows the
// guard supplying what the protocol doesn't: mandatory short TTLs, real
// delegation-chain enforcement, gated renewal as the off-switch, and a local
// blocklist as the emergency brake.

import { generateIdentity } from "./src/identity.mjs";
import { issue, verify, tokenId } from "./src/ucan.mjs";
import { cap, CAP } from "./src/caps.mjs";
import { RevocationStore } from "./src/revocation.mjs";
import { CapabilityGuard } from "./src/guard.mjs";

const log = (s = "") => console.log(s);
const ok = (s) => log(`  ✓ ${s}`);
const no = (s) => log(`  ✗ ${s}`);
const h = (s) => log(`\n── ${s} ──`);

// ── Actors ───────────────────────────────────────────────────────────────
const operator = generateIdentity("operator"); // the human / root of trust
const agent = generateIdentity("aeon-agent"); // a spawned Aeon instance
const subtask = generateIdentity("subtask"); // a short-lived child task

const revocations = new RevocationStore(); // in-memory for the demo
const guard = new CapabilityGuard({
  trustedRoots: new Set([operator.did]),
  revocations,
});

log("Actors:");
log(`  operator : ${operator.did}`);
log(`  agent    : ${agent.did}`);
log(`  subtask  : ${subtask.did}`);

// ── Gap 1: GitLawb makes `exp` optional → no-exp tokens never expire ───────
h("Gap 1 — mandatory expiry (GitLawb allows never-expiring tokens)");
try {
  issue({ issuer: operator, audienceDid: agent.did, capabilities: [cap("*", CAP.REPO_ADMIN)] });
  no("minted a token with no TTL (should be impossible)");
} catch (e) {
  ok(`refused to mint a no-expiry repo/admin token: "${e.message}"`);
}

// ── Gap 2: safety-critical caps are clamped to a short ceiling ─────────────
h("TTL ceiling — dangerous caps get a short leash");
const deployToken = guard.mint({
  issuer: operator,
  audienceDid: agent.did,
  capabilities: [cap("*", CAP.AGENT_DEPLOY), cap("repo:aeon/*", CAP.PR_MERGE)],
  ttlSeconds: 24 * 60 * 60, // ask for 24h...
});
const ttl = deployToken.payload.exp - deployToken.payload.nbf;
ok(`requested 24h for agent/deploy, guard clamped to ${ttl}s (${ttl / 60}min)`);

// ── Gap 3: v0.1 doesn't walk the chain — we do ─────────────────────────────
h("Delegation-chain enforcement (GitLawb v0.1 skips this)");

// Legit attenuation: agent delegates a narrower pr/merge to the subtask.
const merged = guard.delegate({
  issuer: agent,
  audienceDid: subtask.did,
  capabilities: [cap("repo:aeon/bot", CAP.PR_MERGE)],
  ttlSeconds: 120,
  proof: deployToken,
});
let r = guard.authorize(merged, cap("repo:aeon/bot", CAP.PR_MERGE));
r.allowed ? ok("subtask's attenuated pr/merge verified through the full chain")
          : no(`unexpected: ${r.reason}`);

// Escalation attempt: subtask never received repo/admin — forge a delegation.
const escalated = guard.delegate({
  issuer: agent,
  audienceDid: subtask.did,
  capabilities: [cap("*", CAP.REPO_ADMIN)], // not held by agent!
  ttlSeconds: 120,
  proof: deployToken,
});
r = guard.authorize(escalated, cap("*", CAP.REPO_ADMIN));
r.allowed ? no("escalation slipped through!")
          : ok(`privilege escalation rejected at the bridge: "${r.reason}"`);

// Untrusted root: a token whose chain doesn't root in the operator.
const rogueRoot = generateIdentity("rogue");
const forged = issue({
  issuer: rogueRoot,
  audienceDid: subtask.did,
  capabilities: [cap("*", CAP.AGENT_DEPLOY)],
  ttlSeconds: 120,
});
r = guard.authorize(forged, cap("*", CAP.AGENT_DEPLOY));
r.allowed ? no("trusted an unknown root!")
          : ok(`token from an untrusted root rejected: "${r.reason}"`);

// ── Gap 4: renewal-gating is the off-switch revocation can't be ────────────
h("Gated renewal — the off-switch");

const redTeamPass = async () => ({ pass: true });
const redTeamFail = async () => ({ pass: false, reason: "alignment_check_flagged" });

let renew = await guard.renew(
  { priorToken: deployToken, issuer: operator, audienceDid: agent.did,
    capabilities: [cap("*", CAP.AGENT_DEPLOY)], ttlSeconds: 300 },
  redTeamPass,
);
renew.renewed ? ok(`red-team passed → agent/deploy renewed (new exp in 5min)`)
              : no(`unexpected: ${renew.reason}`);

renew = await guard.renew(
  { priorToken: deployToken, issuer: operator, audienceDid: agent.did,
    capabilities: [cap("*", CAP.AGENT_DEPLOY)], ttlSeconds: 300 },
  redTeamFail,
);
renew.renewed ? no("renewed a flagged agent!")
              : ok(`red-team flagged the agent → renewal refused ("${renew.reason}"); cap dies at expiry`);

// ── Emergency brake: blocklist a compromised identity ──────────────────────
h("Revocation blocklist — the emergency brake");
revocations.revokeDid(agent.did, "key suspected compromised");
r = guard.authorize(merged, cap("repo:aeon/bot", CAP.PR_MERGE));
r.allowed ? no("revoked identity still authorized!")
          : ok(`every token in the agent's chain now denied: "${r.reason}"`);

// ── Expiry as the ultimate stop (works even with no revocation) ────────────
h("Expiry — the stop that needs no cooperation");
const future = deployToken.payload.exp + 1;
const v = verify(merged, { now: future });
v.ok ? no("token still valid past expiry!")
     : ok(`past expiry, the token is dead with zero coordination: "${v.reason}"`);

log(`\nDone. Token id sample: ${tokenId(deployToken)}`);
