/**
 * wake-up-stack.test.mjs — Tests for wake-up stack.
 *
 * Run: node scripts/fleet-executors/wake-up-stack.test.mjs
 */

import { WakeUpStack, segmentQuery, keywordOverlap } from "./wake-up-stack.mjs";

let passed = 0;
let failed = 0;

function assert(condition, label) {
  if (condition) {
    passed++;
    console.log(`  ✓ ${label}`);
  } else {
    failed++;
    console.error(`  ✗ ${label}`);
  }
}

// ── segmentQuery ─────────────────────────────────────────────

console.log("segmentQuery:");
{
  // Short task — no segments
  const short = segmentQuery("fix the bug");
  assert(short.full === "fix the bug", "full preserved");
  assert(short.segments.length === 0, "short task has no segments");

  // Long task — generates segments
  const long = segmentQuery(
    "Research the top 3 JavaScript ORMs and compare them on performance, " +
    "ease of use, TypeScript support, and community adoption for a new project"
  );
  assert(long.full.length > 60, "long task preserved");
  assert(long.segments.length > 0, "long task has segments");
  assert(long.segments.length <= 3, "respects maxSegments");

  // Entity extraction
  const withEntities = segmentQuery("check #security issues in the React component and @john's PR");
  assert(withEntities.entities.includes("#security"), "extracts hashtag");
  assert(withEntities.entities.includes("@john"), "extracts mention");

  // Capitalized phrase extraction (multi-word: "Community Adoption", "Base Chain")
  const withCaps = segmentQuery("compare Community Adoption and Base Chain metrics");
  assert(withCaps.entities.some(e => e.includes("Community Adoption") || e.includes("Base Chain")), "extracts capitalized phrase");

  // Question anchor extraction
  const withQuestion = segmentQuery("how do i configure the database connection for PostgreSQL");
  assert(withQuestion.questions.length > 0, "extracts question anchor");
  assert(withQuestion.questions.some(q => q.includes("database")), "question contains key phrase");

  // Empty/null handling
  const empty = segmentQuery("");
  assert(empty.full === "", "empty string handled");
  const nil = segmentQuery(null);
  assert(nil.full === "", "null handled");
}

// ── keywordOverlap ───────────────────────────────────────────

console.log("\nkeywordOverlap:");
{
  // Identical text
  assert(keywordOverlap("hello world", "hello world") === 1, "identical = 1.0");

  // No overlap
  assert(keywordOverlap("apple banana", "xylophone zebra") === 0, "no overlap = 0");

  // Partial overlap: {security,review,codebase} ∩ {security,best,practices,guide} = {security}
  const partial = keywordOverlap("security review of the codebase", "security best practices guide");
  assert(partial > 0 && partial < 1, "partial overlap is between 0 and 1");
  assert(Math.abs(partial - 1 / 3) < 0.01, "one of three keywords overlaps");

  // Stopwords don't count
  assert(keywordOverlap("the the the", "the the the") === 0, "all stopwords = 0");

  // Empty handling
  assert(keywordOverlap("", "hello") === 0, "empty task = 0");
  assert(keywordOverlap("hello", "") === 0, "empty context = 0");
  assert(keywordOverlap(null, "hello") === 0, "null task = 0");
}

// ── WakeUpStack — L0 identity ────────────────────────────────

console.log("\nWakeUpStack — L0:");
{
  const stack = new WakeUpStack({
    identity: { role: "code reviewer", domains: ["security", "performance"] },
  });

  const ctx = await stack.getContext("hello");
  assert(ctx.l0.includes("code reviewer"), "L0 contains role");
  assert(ctx.l0.includes("security"), "L0 contains domain");
  assert(ctx.markdown.includes("## Identity"), "markdown has identity section");
}

// ── WakeUpStack — L1 essentials ──────────────────────────────

console.log("\nWakeUpStack — L1:");
{
  let l1Calls = 0;

  const stack = new WakeUpStack({
    identity: { role: "agent", domains: [] },
    retrieveEssentials: async () => {
      l1Calls++;
      return [
        { text: "JavaScript best practices", score: 0.9 },
        { text: "Node.js performance tips", score: 0.8 },
      ];
    },
  });

  const ctx = await stack.getContext("test");
  assert(ctx.l1.length === 2, "L1 has 2 items");
  assert(ctx.l1[0].text.includes("JavaScript"), "L1 contains expected item");
  assert(l1Calls === 1, "L1 fetched once");
  assert(ctx.markdown.includes("## Essentials"), "markdown has essentials section");

  // Second call uses cache
  await stack.getContext("test");
  assert(l1Calls === 1, "L1 cached — no second fetch");
}

// ── WakeUpStack — L1 cache invalidation ──────────────────────

console.log("\nWakeUpStack — L1 cache invalidation:");
{
  let l1Calls = 0;

  const stack = new WakeUpStack({
    identity: { role: "agent", domains: [] },
    retrieveEssentials: async () => {
      l1Calls++;
      return [{ text: "cached", score: 1 }];
    },
  });

  await stack.getContext("test");
  assert(l1Calls === 1, "fetched once");

  stack.invalidateL1();
  await stack.getContext("test");
  assert(l1Calls === 2, "invalidated — fetched again");
}

// ── WakeUpStack — L2 skipped when overlap is high ────────────

console.log("\nWakeUpStack — L2 skipped (high overlap):");
{
  let l2Calls = 0;

  const stack = new WakeUpStack({
    identity: { role: "agent", domains: ["security"] },
    retrieveEssentials: async () => [
      { text: "security audit checklist and best practices", score: 0.9 },
    ],
    retrieveOnDemand: async (query) => {
      l2Calls++;
      return [{ text: "deep security analysis", score: 0.8 }];
    },
    overlapThreshold: 0.2,
  });

  // Task has "security" which overlaps with L1
  await stack.getContext("review this code for security issues");
  assert(l2Calls === 0, "L2 skipped — security keyword overlaps");
}

// ── WakeUpStack — L2 triggered when divergence detected ──────

console.log("\nWakeUpStack — L2 triggered (divergence):");
{
  let l2Calls = 0;
  let l2Query = "";

  const stack = new WakeUpStack({
    identity: { role: "agent", domains: ["javascript"] },
    retrieveEssentials: async () => [
      { text: "JavaScript best practices for Node.js", score: 0.9 },
    ],
    retrieveOnDemand: async (query) => {
      l2Calls++;
      l2Query = query;
      return [{ text: "Kubernetes deployment guide", score: 0.7 }];
    },
    overlapThreshold: 0.2,
  });

  // Task is about Kubernetes — diverges from L1 (JavaScript)
  const ctx = await stack.getContext("deploy the application to Kubernetes cluster");
  assert(l2Calls === 1, "L2 triggered — topic diverges");
  assert(ctx.l2.length === 1, "L2 returned item");
  assert(ctx.markdown.includes("## Context"), "markdown has context section");
  assert(l2Query.includes("Kubernetes"), "L2 query contains task content");
}

// ── WakeUpStack — L2 uses query segmentation ─────────────────

console.log("\nWakeUpStack — L2 uses segmentation:");
{
  let l2Query = "";

  const stack = new WakeUpStack({
    identity: { role: "agent", domains: ["cooking"] },
    retrieveEssentials: async () => [{ text: "cooking recipes", score: 0.9 }],
    retrieveOnDemand: async (query) => {
      l2Query = query;
      return [{ text: "result", score: 0.5 }];
    },
    overlapThreshold: 0.5, // high threshold to force L2
  });

  await stack.getContext("how do i configure PostgreSQL connection pooling for production");
  // Query should include the task + extracted question phrase
  assert(l2Query.includes("PostgreSQL"), "query includes entity");
  assert(l2Query.includes("configure"), "query includes question anchor word");
}

// ── WakeUpStack — empty/missing providers ────────────────────

console.log("\nWakeUpStack — graceful fallbacks:");
{
  const stack = new WakeUpStack({
    identity: { role: "agent", domains: [] },
    // No providers — should not throw
  });

  const ctx = await stack.getContext("test task");
  assert(ctx.l1.length === 0, "no L1 provider → empty L1");
  assert(ctx.l2.length === 0, "no L2 provider → empty L2");
  assert(ctx.markdown.includes("## Identity"), "markdown still has identity");
}

// ── WakeUpStack — L1 fetch failure ───────────────────────────

console.log("\nWakeUpStack — L1 failure:");
{
  const stack = new WakeUpStack({
    identity: { role: "agent", domains: [] },
    retrieveEssentials: async () => { throw new Error("network error"); },
    verbose: false,
  });

  const ctx = await stack.getContext("test");
  assert(ctx.l1.length === 0, "L1 failure → empty L1 (no crash)");
}

// ── WakeUpStack — L2 failure ────────────────────────────────

console.log("\nWakeUpStack — L2 failure:");
{
  const stack = new WakeUpStack({
    identity: { role: "agent", domains: ["x"] },
    retrieveEssentials: async () => [{ text: "unrelated content", score: 0.5 }],
    retrieveOnDemand: async () => { throw new Error("search failed"); },
    overlapThreshold: 0.9, // force L2
    verbose: false,
  });

  const ctx = await stack.getContext("completely different topic");
  assert(ctx.l2.length === 0, "L2 failure → empty L2 (no crash)");
}

// ── WakeUpStack — L1 TTL expiry ──────────────────────────────

console.log("\nWakeUpStack — L1 TTL expiry:");
{
  let l1Calls = 0;

  const stack = new WakeUpStack({
    identity: { role: "agent", domains: [] },
    retrieveEssentials: async () => {
      l1Calls++;
      return [{ text: "data", score: 1 }];
    },
    l1TtlMs: 50, // 50ms TTL for testing
  });

  await stack.getContext("test");
  assert(l1Calls === 1, "first fetch");

  // Wait for TTL to expire
  await new Promise(r => setTimeout(r, 60));

  await stack.getContext("test");
  assert(l1Calls === 2, "expired — fetched again");
}

// ── segmentQuery integration with WakeUpStack ────────────────

console.log("\nsegmentQuery integration:");
{
  const q = segmentQuery(
    "Research #security vulnerabilities in @company's React Native app and " +
    "how do i fix the Buffer Overflow issue"
  );
  assert(q.entities.includes("#security"), "segmentation: hashtag");
  assert(q.entities.includes("@company"), "segmentation: mention");
  assert(q.questions.length > 0, "segmentation: question anchor");
  assert(q.questions.some(x => x.toLowerCase().includes("buffer")), "segmentation: question content");
}

// ── Results ──────────────────────────────────────────────────

console.log(`\n${passed} passed, ${failed} failed`);
if (failed > 0) throw new Error(`${failed} test(s) failed`);
