// Bridge — the long-running enforcement service.
//
// GitLawb v0.1 "does not yet walk the full UCAN delegation chain; any
// registered agent with a valid HTTP Signature can push." So we do not trust
// the node to reject anything. The bridge re-checks EVERY write event before
// Aeon acts on it:
//
//   1. RFC 9421 HTTP signature valid?            (who is asking, right now)
//   2. sender == signature keyid == token audience?  (token bound to sender)
//   3. UCAN chain authorizes the required cap?   (guard: walk + attenuate +
//                                                 revocation check)
//
// Only events that pass all three are forwarded to Aeon's action layer. The
// merge-gate for self-evolution stays on the GitHub side in Phase 1 — the
// bridge governs reads/writes to the private GitLawb node.

import { CapabilityGuard } from "./guard.mjs";
import { RevocationStore } from "./revocation.mjs";
import { FleetStore } from "./store.mjs";
import { verifyRequest } from "./httpsig.mjs";
import { verifyBytes } from "./identity.mjs";
import { deserializeToken, nowSec } from "./ucan.mjs";
import { cap, CAP } from "./caps.mjs";
import { proposalHash } from "./evolution.mjs";

// Map a node event to the capability it requires.
function defaultActionToCap(event) {
  switch (event.action) {
    case "push":
      return cap(`repo:${event.repo}`, CAP.GIT_PUSH);
    case "fetch":
      return cap(`repo:${event.repo}`, CAP.GIT_FETCH);
    case "pr-merge":
      return cap(`repo:${event.repo}`, CAP.PR_MERGE);
    case "deploy":
      return cap("*", CAP.AGENT_DEPLOY);
    default:
      return null;
  }
}

// Case-insensitive header lookup (HTTP stacks may lowercase keys).
function headerValue(headers, name) {
  if (headers?.[name] != null) return headers[name];
  const lower = name.toLowerCase();
  for (const k of Object.keys(headers ?? {})) if (k.toLowerCase() === lower) return headers[k];
  return undefined;
}

export class Bridge {
  constructor({ guard, actionToCap = defaultActionToCap, maxSigAgeSeconds = 300, enforceMergeCaveat = true, nodeTrust = null, metrics = null, onDecision } = {}) {
    this.guard = guard;
    this.actionToCap = actionToCap;
    this.maxSigAgeSeconds = maxSigAgeSeconds;
    this.enforceMergeCaveat = enforceMergeCaveat;
    this.nodeTrust = nodeTrust; // optional NodeTrustPolicy (Phase 4 economic gate)
    this.metrics = metrics;
    this.onDecision = onDecision;
  }

  handle(event, { now = nowSec() } = {}) {
    const base = { action: event.action, repo: event.repo, ref: event.ref, sender: event.sender };
    const deny = (reason) => this.#emit({ ...base, decision: "deny", reason });
    const allow = (capabilities) => this.#emit({ ...base, decision: "allow", capabilities });

    // 0. Economic gate: will we accept events relayed by this node at all?
    // (Phase 4 — a rogue node needs real stake, a live heartbeat, and no slash.)
    // The node id must be AUTHENTICATED: the relay signs the request it carries
    // with its own key, so an unstaked node can't claim a staked node's id.
    if (this.nodeTrust) {
      const sig = headerValue(event.request.headers, "Signature");
      if (!event.node || !event.nodeSig || !sig) return deny("node_unauthenticated:missing");
      if (!verifyBytes(event.node, sig, Buffer.from(event.nodeSig, "base64"))) {
        return deny("node_unauthenticated:bad_signature");
      }
      const nt = this.nodeTrust.evaluate(event.node, { now });
      if (!nt.trusted) return deny(`node_untrusted:${nt.reason}`);
    }

    // 1. Request-level authentication.
    const sig = verifyRequest({ ...event.request, maxAgeSeconds: this.maxSigAgeSeconds, now });
    if (!sig.ok) return deny(`http_sig:${sig.reason}`);

    // 2. Bind the request to the capability holder.
    if (sig.keyid !== event.sender) return deny("sender_keyid_mismatch");
    const token = deserializeToken(event.token);
    if (token.payload.aud !== event.sender) return deny("sender_not_audience");

    // 3. Capability authorization (chain walk + attenuation + revocation).
    const required = this.actionToCap(event);
    if (!required) return deny(`unknown_action:${event.action}`);
    const auth = this.guard.authorize(token, required, { now });
    if (!auth.allowed) return deny(`cap:${auth.reason}`);

    // Phase 3 defense-in-depth: a self-evolution merge must carry a pr/merge
    // capability whose caveat is bound to the exact change being merged. (In
    // GitLawb v0.2 the node enforces this server-side; the bridge mirrors it.)
    if (event.action === "pr-merge" && this.enforceMergeCaveat) {
      const denyMerge = this.#checkMergeCaveat(event, auth.capabilities);
      if (denyMerge) return deny(denyMerge);
    }

    return allow(auth.capabilities);
  }

  // Subscribe to a source and enforce every event it yields.
  async run(source, opts = {}) {
    const decisions = [];
    await source.subscribe((event) => {
      decisions.push(this.handle(event, opts));
    });
    return decisions;
  }

  // Returns a deny-reason string if the merge caveat doesn't bind to the
  // proposal carried in the (signed) request body, else null.
  #checkMergeCaveat(event, capabilities) {
    let proposal;
    try {
      proposal = JSON.parse(event.request.body).proposal;
    } catch {
      return "merge_gate:unparseable_body";
    }
    if (!proposal) return "merge_gate:missing_proposal";

    const merge = capabilities.find((c) => c.can === CAP.PR_MERGE && c.nb);
    if (!merge) return "merge_gate:uncaveated_merge_cap";
    if (merge.nb.proposal !== proposalHash(proposal)) return "merge_gate:proposal_caveat_mismatch";
    if (merge.nb.ref !== proposal.ref) return "merge_gate:ref_caveat_mismatch";
    return null;
  }

  #emit(decision) {
    this.metrics?.record("bridge", { action: decision.action, decision: decision.decision, reason: decision.reason ?? "ok" });
    if (this.onDecision) this.onDecision(decision);
    return decision;
  }
}

// Wire a bridge from on-disk fleet state so it shares the operator trust root
// and the SAME revocation store the gitlawb-fleet `kill` writes to — a kill
// propagates to bridge decisions with no extra plumbing.
//
// The revocation store is file-backed here (survives restart). Production
// swaps it for Postgres/SQLite behind the same interface; the bridge is
// unchanged.
export function createBridgeFromStore({ registryPath, vaultPath, revocationsPath, ...opts }) {
  const store = new FleetStore({ registryPath, vaultPath });
  const revocations = new RevocationStore(revocationsPath);
  const operator = store.getMeta().operator;
  if (!operator) throw new Error("no operator in registry — run `fleet-cli.mjs init` first");
  const guard = new CapabilityGuard({ trustedRoots: new Set([operator]), revocations });
  return new Bridge({ guard, ...opts });
}

export { defaultActionToCap };
