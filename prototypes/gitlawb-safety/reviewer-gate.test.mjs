// Tests for the reviewer-routed renewal gate + its policy integration.
// Run: node prototypes/gitlawb-safety/reviewer-gate.test.mjs

import { mkdtempSync, writeFileSync, rmSync } from "node:fs";
import { join } from "node:path";
import { tmpdir } from "node:os";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import { dirname } from "node:path";
import { makeReviewerGate, activityFingerprint } from "./src/reviewer-gate.mjs";
import { makePolicyCheck } from "./src/policy.mjs";

const HERE = dirname(fileURLToPath(import.meta.url));
let passed = 0, failed = 0;
const ok = (c, label) => (c ? (passed++, console.log(`  ✓ ${label}`)) : (failed++, console.error(`  ✗ ${label}`)));

const REVIEWER = "did:key:reviewer";
const AGENT = "did:key:deployer";
const SAFETY_CAP = [{ can: "agent/deploy", with: "*" }];
const ctx = { audienceDid: AGENT, capabilities: SAFETY_CAP, activity: { changedFiles: ["skills/x/SKILL.md"], changedLines: 10 } };

// `false` always exits non-zero → no real gl call; dispatch logs a soft fail.
const GL = "false";

function writeVerdict(dir, { taskId, targetDid, fp, line, completedAt, byDid = REVIEWER }) {
  writeFileSync(join(dir, `${taskId}.json`), JSON.stringify({
    task: { id: taskId, kind: "renewal-review", payload: JSON.stringify({ target_did: targetDid, fingerprint: fp }) },
    instance: { did: byDid }, // who executed the review — must be the reviewer
    result: { summary: line },
    completed_at: completedAt ?? new Date().toISOString(),
  }));
}

console.log("activityFingerprint:");
{
  const a = activityFingerprint(ctx);
  const b = activityFingerprint({ ...ctx, activity: { changedFiles: ["skills/x/SKILL.md"], changedLines: 10 } });
  const c = activityFingerprint({ ...ctx, activity: { changedFiles: ["other.md"], changedLines: 10 } });
  ok(a === b, "stable for identical activity");
  ok(a !== c, "differs when files differ");
}

console.log("\nGate — no verdict yet:");
{
  const dir = mkdtempSync(join(tmpdir(), "rg-"));
  const gate = makeReviewerGate({ reviewerDid: REVIEWER, artifactsDir: dir, glBin: GL });
  const r = await gate(ctx);
  ok(r.pass === false && r.reason === "review_pending", "fails closed with review_pending");
  rmSync(dir, { recursive: true });
}

console.log("\nGate — fresh approved verdict:");
{
  const dir = mkdtempSync(join(tmpdir(), "rg-"));
  const fp = activityFingerprint(ctx);
  writeVerdict(dir, { taskId: "t1", targetDid: AGENT, fp, line: `RENEWAL_VERDICT approved fp=${fp}` });
  const gate = makeReviewerGate({ reviewerDid: REVIEWER, artifactsDir: dir, glBin: GL });
  const r = await gate(ctx);
  ok(r.pass === true && r.reason === "reviewer_lgtm", "passes on fresh LGTM");
  rmSync(dir, { recursive: true });
}

console.log("\nGate — flagged verdict:");
{
  const dir = mkdtempSync(join(tmpdir(), "rg-"));
  const fp = activityFingerprint(ctx);
  writeVerdict(dir, { taskId: "t2", targetDid: AGENT, fp, line: `RENEWAL_VERDICT denied:oversight_tampering fp=${fp}` });
  const gate = makeReviewerGate({ reviewerDid: REVIEWER, artifactsDir: dir, glBin: GL });
  const r = await gate(ctx);
  ok(r.pass === false && r.reason === "reviewer:oversight_tampering", "denies on flagged verdict");
  rmSync(dir, { recursive: true });
}

console.log("\nGate — forged verdict (not from reviewer) is rejected:");
{
  const dir = mkdtempSync(join(tmpdir(), "rg-"));
  const fp = activityFingerprint(ctx);
  // Agent forges its own approval artifact, attributing it to itself.
  writeVerdict(dir, { taskId: "forge", targetDid: AGENT, fp, line: `RENEWAL_VERDICT approved fp=${fp}`, byDid: AGENT });
  const gate = makeReviewerGate({ reviewerDid: REVIEWER, artifactsDir: dir, glBin: GL });
  const r = await gate(ctx);
  ok(r.pass === false && r.reason === "review_pending", "verdict not authored by reviewer is ignored");
  rmSync(dir, { recursive: true });
}

console.log("\nGate — verdict for different activity is ignored:");
{
  const dir = mkdtempSync(join(tmpdir(), "rg-"));
  writeVerdict(dir, { taskId: "t3", targetDid: AGENT, fp: "deadbeefdeadbeef", line: `RENEWAL_VERDICT approved fp=deadbeefdeadbeef` });
  const gate = makeReviewerGate({ reviewerDid: REVIEWER, artifactsDir: dir, glBin: GL });
  const r = await gate(ctx);
  ok(r.pass === false && r.reason === "review_pending", "stale-fingerprint verdict not accepted");
  rmSync(dir, { recursive: true });
}

console.log("\nGate — stale (old) verdict expires:");
{
  const dir = mkdtempSync(join(tmpdir(), "rg-"));
  const fp = activityFingerprint(ctx);
  const old = new Date(Date.now() - 2 * 3600 * 1000).toISOString();
  writeVerdict(dir, { taskId: "t4", targetDid: AGENT, fp, line: `RENEWAL_VERDICT approved fp=${fp}`, completedAt: old });
  const gate = makeReviewerGate({ reviewerDid: REVIEWER, artifactsDir: dir, glBin: GL, freshSeconds: 3600 });
  const r = await gate(ctx);
  ok(r.pass === false && r.reason === "review_pending", "verdict older than freshSeconds ignored");
  rmSync(dir, { recursive: true });
}

console.log("\nGate — reviewer self-renewal exemption:");
{
  const dir = mkdtempSync(join(tmpdir(), "rg-"));
  const gate = makeReviewerGate({ reviewerDid: REVIEWER, artifactsDir: dir, glBin: GL });
  const r = await gate({ ...ctx, audienceDid: REVIEWER });
  ok(r.pass === true && r.reason === "reviewer_self_rules_only", "reviewer renews on rules only");
  rmSync(dir, { recursive: true });
}

console.log("\nGate — no reviewerDid → null (rules-only fallback):");
ok(makeReviewerGate({ reviewerDid: null }) === null, "returns null without a reviewer");

console.log("\nPolicy integration:");
{
  const dir = mkdtempSync(join(tmpdir(), "rg-"));
  const fp = activityFingerprint(ctx);
  writeVerdict(dir, { taskId: "t5", targetDid: AGENT, fp, line: `RENEWAL_VERDICT approved fp=${fp}` });
  const gate = makeReviewerGate({ reviewerDid: REVIEWER, artifactsDir: dir, glBin: GL });
  const check = makePolicyCheck({ redTeam: gate });

  const rPass = await check(ctx);
  ok(rPass.pass === true, "rules pass + reviewer LGTM → renew");

  // Rules reject BEFORE the red-team ever runs (protected path).
  const rProtected = await check({ ...ctx, activity: { changedFiles: ["prototypes/gitlawb-safety/src/policy.mjs"], changedLines: 2 } });
  ok(rProtected.pass === false && rProtected.reason.startsWith("touched_protected_path"), "rule layer blocks oversight tampering first");

  // Red-team error fails closed.
  const errCheck = makePolicyCheck({ redTeam: async () => { throw new Error("boom"); } });
  const rErr = await errCheck(ctx);
  ok(rErr.pass === false && rErr.reason === "redteam_error", "red-team error fails closed");
  rmSync(dir, { recursive: true });
}

console.log("\nReviewer renewal-review branch (live invocation):");
{
  const reviewer = join(HERE, "..", "..", "scripts", "fleet-executors", "reviewer.mjs");
  const mk = (payload) => spawnSync("node", [reviewer], {
    encoding: "utf8",
    env: { ...process.env,
      GITLAWB_TASK_JSON: JSON.stringify({ id: "rv", kind: "renewal-review", payload: JSON.stringify(payload) }),
      GITLAWB_AGENT_JSON: JSON.stringify({ name: "aeon-reviewer" }) },
  });
  const clean = mk({ review_kind: "renewal", target_did: AGENT, fingerprint: "abc123", changedFiles: ["skills/x.md"], changedLines: 5, capabilities: ["agent/deploy"] });
  ok(/^RENEWAL_VERDICT approved fp=abc123/m.test(clean.stdout), "clean activity → approved");
  const tamper = mk({ review_kind: "renewal", target_did: AGENT, fingerprint: "abc123", changedFiles: [".github/workflows/x.yml"], changedLines: 5 });
  ok(/RENEWAL_VERDICT denied:oversight_tampering fp=abc123/.test(tamper.stdout), "workflow edit → denied:oversight_tampering");
}

console.log(`\n${passed} passed, ${failed} failed`);
process.exit(failed > 0 ? 1 : 0);
