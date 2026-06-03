// SelfEvolutionGate — the portable replacement for GitHub branch protection.
//
// Aeon's safety today is GitHub centralization: a self-evolution PR can't merge
// until required checks pass. On GitLawb there's no central repo to protect, so
// we model "permission to merge THIS change" as a capability:
//
//   1. An agent proposes a self-evolution (a diff to its own skills/config).
//   2. The gate runs an automated policy check, then a red-team review.
//   3. Only on approval does the operator mint a SHORT-LIVED `pr/merge` UCAN —
//      and it is bound, via a caveat, to the hash of THAT exact proposal.
//   4. A merge is authorized only if the presented capability's caveat matches
//      the change being merged. An approval for one diff cannot merge another.
//
// `authorizeMerge` is what a GitLawb v0.2 node enforces server-side (once it
// walks the chain). Until then the bridge runs it as defense-in-depth. Either
// way it needs no GitHub repo — the gate is portable across nodes.

import { createHash } from "node:crypto";
import { cap, CAP } from "./caps.mjs";
import { nowSec } from "./ucan.mjs";
import { makePolicyCheck } from "./policy.mjs";

// Stable hash binding an approval to a specific change. Includes the diff
// digest so two PRs touching the same files but different content differ.
export function proposalHash(p) {
  const basis = {
    repo: p.repo,
    ref: p.ref,
    changedFiles: [...(p.changedFiles ?? [])].sort(),
    diffDigest: p.diffDigest ?? "",
  };
  return "ph_" + createHash("sha256").update(JSON.stringify(basis)).digest("base64url").slice(0, 22);
}

export class SelfEvolutionGate {
  constructor({ operator, guard, redTeam, policyCheck = makePolicyCheck(), mergeTtlSeconds = 120, metrics = null }) {
    this.operator = operator;
    this.guard = guard;
    this.redTeam = redTeam;
    this.policyCheck = policyCheck;
    this.mergeTtlSeconds = mergeTtlSeconds;
    this.metrics = metrics;
  }

  // Review a proposed self-evolution. Returns an approval with a caveat-bound
  // merge capability, or a refusal naming the stage that blocked it.
  async review(proposal, redTeam = this.redTeam) {
    const mergeCap = cap(`repo:${proposal.repo}`, CAP.PR_MERGE);

    // Stage 1 — automated policy (path allowlist, protected paths, diff size).
    const pol = await this.policyCheck({
      audienceDid: proposal.agentDid,
      capabilities: [mergeCap],
      activity: { changedFiles: proposal.changedFiles, changedLines: proposal.changedLines },
    });
    if (!pol.pass) {
      this.metrics?.record("review", { approved: false, stage: "policy", reason: pol.reason, repo: proposal.repo });
      return { approved: false, stage: "policy", reason: pol.reason };
    }

    // Stage 2 — red-team review (a sub-swarm in production; pluggable here).
    const rt = await redTeam(proposal);
    if (!rt.pass) {
      this.metrics?.record("review", { approved: false, stage: "red-team", reason: rt.reason, repo: proposal.repo });
      return { approved: false, stage: "red-team", reason: rt.reason, findings: rt.findings };
    }

    // Mint a short-lived pr/merge cap bound to THIS proposal only.
    const ph = proposalHash(proposal);
    const mergeToken = this.guard.mint({
      issuer: this.operator,
      audienceDid: proposal.agentDid,
      capabilities: [cap(`repo:${proposal.repo}`, CAP.PR_MERGE, { proposal: ph, ref: proposal.ref })],
      ttlSeconds: this.mergeTtlSeconds,
    });
    this.metrics?.record("review", { approved: true, repo: proposal.repo, proposal: ph });
    return { approved: true, mergeToken, proposalHash: ph, expiresAt: mergeToken.payload.exp };
  }

  // Authorize an actual merge. Node-side in v0.2; bridge-side today.
  authorizeMerge({ token, proposal, now = nowSec() }) {
    const res = this.#authorizeMerge({ token, proposal, now });
    this.metrics?.record("merge_authorize", { allowed: res.allowed, reason: res.reason ?? "ok", repo: proposal.repo });
    return res;
  }

  #authorizeMerge({ token, proposal, now }) {
    const auth = this.guard.authorize(token, cap(`repo:${proposal.repo}`, CAP.PR_MERGE), { now });
    if (!auth.allowed) return { allowed: false, reason: auth.reason };

    // Caveat binding — the approval must be for exactly this change.
    const ph = proposalHash(proposal);
    const merge = auth.capabilities.find((c) => c.can === CAP.PR_MERGE && c.nb);
    if (!merge) return { allowed: false, reason: "uncaveated_merge_cap" };
    if (merge.nb.proposal !== ph) return { allowed: false, reason: "proposal_caveat_mismatch" };
    if (merge.nb.ref !== proposal.ref) return { allowed: false, reason: "ref_caveat_mismatch" };
    return { allowed: true };
  }
}
