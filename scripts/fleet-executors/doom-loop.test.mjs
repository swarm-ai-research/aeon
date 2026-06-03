/**
 * doom-loop.test.mjs — Tests for the doom loop detector.
 *
 * Run: node scripts/fleet-executors/doom-loop.test.mjs
 */

import { DoomLoopDetector, buildCorrectivePrompt } from "./doom-loop.mjs";

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

// ── Test 1: No loop with fewer than threshold calls ──────────

console.log("Test 1: Below threshold");
{
  const d = new DoomLoopDetector({ threshold: 3 });
  d.record("git_commit", { message: "fix" });
  d.record("git_commit", { message: "fix" });
  assert(d.check() === null, "2 identical calls — no loop");
}

// ── Test 2: Identical consecutive triggers ────────────────────

console.log("Test 2: Identical consecutive");
{
  const d = new DoomLoopDetector({ threshold: 3 });
  d.record("git_commit", { message: "fix typo" });
  d.record("git_commit", { message: "fix typo" });
  d.record("git_commit", { message: "fix typo" });
  const result = d.check();
  assert(result !== null, "3 identical calls — loop detected");
  assert(result.offender === "git_commit", "offender is git_commit");
  assert(result.pattern === "identical", "pattern is identical");
  assert(result.corrective.includes("git_commit"), "corrective mentions offender");
}

// ── Test 3: Same tool, different args — no loop ───────────────

console.log("Test 3: Same tool, different args");
{
  const d = new DoomLoopDetector({ threshold: 3 });
  d.record("git_commit", { message: "fix a" });
  d.record("git_commit", { message: "fix b" });
  d.record("git_commit", { message: "fix c" });
  assert(d.check() === null, "same tool, different args — no loop");
}

// ── Test 4: Repeating A→B sequence ───────────────────────────

console.log("Test 4: Repeating A→B sequence");
{
  const d = new DoomLoopDetector({ threshold: 3 });
  d.record("search", { q: "foo" });
  d.record("read_file", { path: "a.txt" });
  d.record("search", { q: "foo" });
  d.record("read_file", { path: "a.txt" });
  const result = d.check();
  assert(result !== null, "A→B→A→B — loop detected");
  assert(result.pattern === "repeating", "pattern is repeating");
  assert(result.message.includes("search → read_file"), "sequence described");
}

// ── Test 5: Repeating A→B→C sequence ─────────────────────────

console.log("Test 5: Repeating A→B→C sequence");
{
  const d = new DoomLoopDetector({ threshold: 3 });
  d.record("search", {});
  d.record("read_file", {});
  d.record("write_file", {});
  d.record("search", {});
  d.record("read_file", {});
  d.record("write_file", {});
  const result = d.check();
  assert(result !== null, "A→B→C→A→B→C — loop detected");
  assert(result.pattern === "repeating", "pattern is repeating");
}

// ── Test 6: No false positive on non-repeating ────────────────

console.log("Test 6: No false positive");
{
  const d = new DoomLoopDetector({ threshold: 3 });
  d.record("search", { q: "a" });
  d.record("read_file", { path: "b" });
  d.record("git_commit", { message: "c" });
  d.record("deploy", {});
  d.record("notify", { msg: "done" });
  assert(d.check() === null, "5 different actions — no loop");
}

// ── Test 7: Lookback window ───────────────────────────────────

console.log("Test 7: Lookback window");
{
  const d = new DoomLoopDetector({ threshold: 3, lookback: 5 });
  d.record("git_commit", { message: "a" });
  d.record("git_commit", { message: "a" });
  // 3 different calls to push old ones out of window
  d.record("x", {});
  d.record("y", {});
  d.record("z", {});
  d.record("w", {});
  d.record("v", {});
  // Now only 2 identical remain in window
  assert(d.check() === null, "old identical calls outside lookback — no loop");
}

// ── Test 8: fromMessages static constructor ───────────────────

console.log("Test 8: fromMessages");
{
  const messages = [
    { role: "user", content: "fix the bug" },
    { role: "assistant", tool_calls: [{ function: { name: "search", arguments: '{"q":"bug"}' } }] },
    { role: "tool", content: "found" },
    { role: "assistant", tool_calls: [{ function: { name: "search", arguments: '{"q":"bug"}' } }] },
    { role: "tool", content: "found" },
    { role: "assistant", tool_calls: [{ function: { name: "search", arguments: '{"q":"bug"}' } }] },
  ];
  const d = DoomLoopDetector.fromMessages(messages, { threshold: 3 });
  const result = d.check();
  assert(result !== null, "3 identical tool calls in messages — loop detected");
  assert(result.offender === "search", "offender is search");
}

// ── Test 9: checkAndClear resets state ────────────────────────

console.log("Test 9: checkAndClear");
{
  const d = new DoomLoopDetector({ threshold: 3 });
  d.record("a", {});
  d.record("a", {});
  d.record("a", {});
  assert(d.checkAndClear() !== null, "first check detects loop");
  assert(d.check() === null, "after clear, no loop");
}

// ── Test 10: reset ────────────────────────────────────────────

console.log("Test 10: reset");
{
  const d = new DoomLoopDetector({ threshold: 2 });
  d.record("a", {});
  d.record("a", {});
  assert(d.check() !== null, "before reset — loop");
  d.reset();
  assert(d.check() === null, "after reset — no loop");
}

// ── Results ──────────────────────────────────────────────────

console.log(`\n${passed} passed, ${failed} failed`);
if (failed > 0) throw new Error(`${failed} test(s) failed`);
