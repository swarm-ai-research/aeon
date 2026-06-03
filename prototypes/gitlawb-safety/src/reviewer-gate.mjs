// Reviewer-routed renewal gate — the red-team stage as a true sub-swarm.
//
// Instead of judging a renewal in-process, this routes the decision to the
// fleet's existing aeon-reviewer agent. It is the pluggable `redTeam` consumed
// by makePolicyCheck (src/policy.mjs), running AFTER the cheap rule checks.
//
// Flow (fail-closed):
//   1. Compute a fingerprint of the activity under review.
//   2. Look for a fresh, completed reviewer verdict for THIS agent + fingerprint
//      in the task artifacts (memory/gitlawb-runner/*.json).
//        • approved  → pass (cap renewed)
//        • flagged   → deny  (cap lapses at its short TTL)
//   3. No fresh verdict → dispatch a `renewal-review` task to aeon-reviewer
//      (gl task create) and DENY this cycle (reason: review_pending). The
//      reviewer picks it up on its next poll; a later renewal cycle reads the
//      verdict. Authority is re-earned across cycles, never assumed.
//
// The reviewer's own renewal can't route to itself (deadlock), so it falls back
// to rules-only — see the reviewerDid guard below.

import { spawnSync } from "node:child_process";
import { createHash } from "node:crypto";
import { existsSync, readFileSync, readdirSync } from "node:fs";
import { join } from "node:path";

const FRESH_SECONDS = 3600; // a verdict older than this no longer counts
const REVIEW_KIND = "renewal-review";

// A stable fingerprint of exactly what is being reviewed, so a verdict only
// counts for the activity it actually saw — not an earlier, different diff.
export function activityFingerprint(ctx) {
  const a = ctx?.activity ?? {};
  const files = [...(a.changedFiles ?? [])].sort();
  return createHash("sha256")
    .update(JSON.stringify({ did: ctx?.audienceDid ?? "", files, lines: a.changedLines ?? 0 }))
    .digest("hex")
    .slice(0, 16);
}

export function makeReviewerGate({
  reviewerDid,
  reviewerName = "aeon-reviewer",
  artifactsDir = "memory/gitlawb-runner",
  node = process.env.GITLAWB_NODE,
  freshSeconds = FRESH_SECONDS,
  glBin = "gl",
  now = () => Date.now(),
} = {}) {
  // Without a reviewer to route to, the caller (fleet-cli) falls back to
  // rules-only — same as before this gate existed.
  if (!reviewerDid) return null;

  return async function reviewerGate(ctx) {
    const fp = activityFingerprint(ctx);

    // The reviewer cannot adversarially review its own renewal — that would
    // deadlock (it must be alive to review, but renewal is what keeps it alive).
    // Rules already passed to reach here, so allow it and flag the exemption.
    if (ctx?.audienceDid === reviewerDid) {
      return { pass: true, reason: "reviewer_self_rules_only" };
    }

    const verdict = findVerdict({ artifactsDir, targetDid: ctx.audienceDid, fingerprint: fp, freshSeconds, now, reviewerDid });
    if (verdict) {
      return verdict.approved
        ? { pass: true, reason: "reviewer_lgtm", reviewedAt: verdict.reviewedAt }
        : { pass: false, reason: verdict.reason || "reviewer_flagged", findings: verdict.findings, stage: "red-team" };
    }

    // No fresh verdict — dispatch a review (deduped) and fail closed this cycle.
    dispatchReview({ glBin, reviewerDid, reviewerName, node, ctx, fingerprint: fp });
    return { pass: false, reason: "review_pending", stage: "red-team" };
  };
}

// Scan completed task artifacts for a fresh renewal-review verdict matching the
// target agent and activity fingerprint. The reviewer writes a parseable line
// `RENEWAL_VERDICT <approved|denied:reason> fp=<fp>` as its first output, which
// lands in result.summary (see reviewer.mjs + task-runner persistArtifact).
function findVerdict({ artifactsDir, targetDid, fingerprint, freshSeconds, now, reviewerDid }) {
  if (!existsSync(artifactsDir)) return null;
  const cutoff = now() - freshSeconds * 1000;
  let best = null;

  for (const file of readdirSync(artifactsDir)) {
    if (!file.endsWith(".json")) continue;
    let rec;
    try {
      rec = JSON.parse(readFileSync(join(artifactsDir, file), "utf8"));
    } catch {
      continue;
    }
    const kind = rec?.task?.kind ?? rec?.task?.type;
    if (kind !== REVIEW_KIND) continue;

    // The verdict is only trustworthy if it was produced by the reviewer. The
    // artifact records the executing instance; require it to be the reviewer so
    // an agent can't self-approve by dropping a forged artifact. (Belt-and-
    // braces: policy.mjs also marks the artifact dir as a protected path so an
    // agent diff can't write here in the first place.)
    if (reviewerDid && rec?.instance?.did !== reviewerDid) continue;

    const payload = parsePayload(rec?.task?.payload);
    if ((payload.target_did ?? payload.targetDid) !== targetDid) continue;

    const completedMs = Date.parse(rec?.completed_at ?? "");
    if (!Number.isFinite(completedMs) || completedMs < cutoff) continue;

    const summary = rec?.result?.summary ?? "";
    // Groups: 1 = approved|denied[:reason], 2 = reason (if denied), 3 = fp.
    const m = summary.match(/RENEWAL_VERDICT\s+(approved|denied(?::([^\s]+))?)\s+fp=([0-9a-f]+)/);
    if (!m) continue;
    if (m[3] !== fingerprint) continue; // verdict was for different activity

    if (!best || completedMs > best.completedMs) {
      best = {
        completedMs,
        approved: m[1] === "approved",
        reason: m[2] ? `reviewer:${m[2]}` : undefined,
        reviewedAt: rec.completed_at,
      };
    }
  }
  return best;
}

// Create a renewal-review task for the reviewer, unless an equivalent one is
// already pending (so we don't pile up a task every 5-minute cycle).
function dispatchReview({ glBin, reviewerDid, reviewerName, node, ctx, fingerprint }) {
  if (pendingReviewExists({ glBin, reviewerDid, node, targetDid: ctx.audienceDid, fingerprint })) {
    return;
  }
  const a = ctx.activity ?? {};
  const payload = {
    title: `Renewal review for ${ctx.audienceDid}`,
    review_kind: "renewal",
    target_did: ctx.audienceDid,
    fingerprint,
    capabilities: (ctx.capabilities ?? []).map((c) => (typeof c === "string" ? c : c.can)),
    changedFiles: a.changedFiles ?? [],
    changedLines: a.changedLines ?? 0,
    purpose: ctx.purpose ?? a.purpose ?? "",
  };
  const args = [
    "task", "create", REVIEW_KIND,
    "--assignee-did", reviewerDid,
    "--capability", "pr:review",
    "--payload", JSON.stringify(payload),
  ];
  if (node) args.push("--node", node);
  const proc = spawnSync(glBin, args, { encoding: "utf8" });
  if (proc.status !== 0) {
    console.log(`REVIEW_DISPATCH_FAIL ${reviewerName} ${ctx.audienceDid} ${(proc.stderr || proc.stdout || "").trim().slice(0, 160)}`);
  } else {
    console.log(`REVIEW_DISPATCHED ${reviewerName} target=${ctx.audienceDid} fp=${fingerprint}`);
  }
}

// True if an equivalent review is already in flight. A task leaves "pending"
// once the reviewer claims it but isn't done, so we must also count claimed/
// in-progress work — otherwise a slow review spawns a duplicate every cycle.
const IN_FLIGHT_STATUSES = ["pending", "claimed", "in_progress", "running"];

function pendingReviewExists({ glBin, reviewerDid, node, targetDid, fingerprint }) {
  // Query without a status filter and exclude only terminal states, so any
  // non-completed review counts regardless of the node's exact status labels.
  const args = ["task", "list", "--assignee-did", reviewerDid, "--limit", "100"];
  if (node) args.push("--node", node);
  const proc = spawnSync(glBin, args, { encoding: "utf8" });
  if (proc.status !== 0) return false; // can't tell → allow dispatch (fail toward reviewing)
  let parsed;
  try {
    parsed = JSON.parse(proc.stdout);
  } catch {
    return false;
  }
  const tasks = Array.isArray(parsed.tasks) ? parsed.tasks : [];
  return tasks.some((t) => {
    if ((t.kind ?? t.type) !== REVIEW_KIND) return false;
    const status = (t.status ?? "pending").toLowerCase();
    const inFlight = IN_FLIGHT_STATUSES.includes(status) || !["completed", "failed", "cancelled", "canceled"].includes(status);
    if (!inFlight) return false;
    const p = parsePayload(t.payload);
    return (p.target_did ?? p.targetDid) === targetDid && p.fingerprint === fingerprint;
  });
}

function parsePayload(payload) {
  if (!payload) return {};
  if (typeof payload === "object") return payload;
  try {
    return JSON.parse(payload);
  } catch {
    return {};
  }
}
