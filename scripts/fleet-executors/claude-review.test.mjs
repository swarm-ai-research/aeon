// claude-review.test.mjs — Unit tests for claudeReview / parseReview / buildPrompt.
//
// Stubs the `claude` CLI binary on PATH so no real network or auth is needed.
// Run: node scripts/fleet-executors/claude-review.test.mjs

import { mkdtempSync, writeFileSync, rmSync, chmodSync, mkdirSync, readFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { spawnSync } from "node:child_process";
import assert from "node:assert/strict";
import { claudeReview } from "./claude-review.mjs";

function makeBin(dir, name, script) {
  const p = join(dir, name);
  writeFileSync(p, script);
  chmodSync(p, 0o755);
  return p;
}

function withStub(claudeStdout, fn) {
  const work = mkdtempSync(join(tmpdir(), "claude-review-test-"));
  const binDir = join(work, "bin");
  mkdirSync(binDir);
  makeBin(binDir, "claude", `#!/usr/bin/env bash
if [ "$1" = "--version" ]; then echo "stub claude 1.0"; exit 0; fi
cat > /dev/null
printf '%s' ${JSON.stringify(claudeStdout)}
`);
  const oldPath = process.env.PATH;
  process.env.PATH = `${binDir}:${oldPath}`;
  try {
    return fn(work);
  } finally {
    process.env.PATH = oldPath;
    rmSync(work, { recursive: true, force: true });
  }
}

function withUnavailableStub(fn) {
  const work = mkdtempSync(join(tmpdir(), "claude-review-test-"));
  const binDir = join(work, "bin");
  mkdirSync(binDir);
  makeBin(binDir, "claude", `#!/usr/bin/env bash\nexit 1\n`);
  const oldPath = process.env.PATH;
  process.env.PATH = `${binDir}:${oldPath}`;
  try {
    return fn(work);
  } finally {
    process.env.PATH = oldPath;
    rmSync(work, { recursive: true, force: true });
  }
}

// 1. null/empty diff → null (no claude invoked)
{
  const result = claudeReview({ diff: null });
  assert.equal(result, null);
  const result2 = claudeReview({ diff: "" });
  assert.equal(result2, null);
  console.log("OK  null/empty diff returns null without calling claude");
}

// 2. claude CLI unavailable (--version exits 1) → null
{
  const result = withUnavailableStub(() =>
    claudeReview({ diff: "--- a\n+++ b\n@@ -1 +1 @@\n-old\n+new" })
  );
  assert.equal(result, null);
  console.log("OK  claude CLI unavailable returns null");
}

// 3. Valid JSON response → structured review object
{
  const payload = JSON.stringify({
    verdict: "approve-ready",
    confidence: 4,
    summary: "Looks good overall.",
    findings: [
      { severity: "ISSUE", file: "foo.js", line: 10, why: "Missing null check." },
    ],
  });
  const result = withStub(payload, () =>
    claudeReview({ diff: "--- a\n+++ b\n@@ -1 +1 @@\n-old\n+new" })
  );
  assert.ok(result !== null, "expected non-null result");
  assert.equal(result.verdict, "approve-ready");
  assert.equal(result.confidence, 4);
  assert.equal(result.summary, "Looks good overall.");
  assert.equal(result.findings.length, 1);
  assert.equal(result.findings[0].severity, "ISSUE");
  assert.equal(result.findings[0].line, 10);
  console.log("OK  valid JSON response → structured review object");
}

// 4. JSON embedded in prose (e.g. claude preamble + JSON + trailing text)
//    parseReview uses indexOf('{') and lastIndexOf('}') to extract the JSON.
{
  const payload =
    "Here is my review:\n" +
    JSON.stringify({ verdict: "discussion-needed", confidence: 3, summary: "Some concerns.", findings: [] }) +
    "\nEnd of review.";
  const result = withStub(payload, () =>
    claudeReview({ diff: "diff text" })
  );
  assert.ok(result !== null);
  assert.equal(result.verdict, "discussion-needed");
  assert.equal(result.findings.length, 0);
  console.log("OK  JSON embedded in prose is extracted via indexOf/lastIndexOf");
}

// 5. claude returns non-JSON text → null
{
  const result = withStub("Sorry, I cannot review this diff.", () =>
    claudeReview({ diff: "diff text" })
  );
  assert.equal(result, null);
  console.log("OK  non-JSON output returns null");
}

// 6. Valid JSON but missing verdict field → null
{
  const payload = JSON.stringify({ confidence: 5, summary: "ok", findings: [] });
  const result = withStub(payload, () =>
    claudeReview({ diff: "diff text" })
  );
  assert.equal(result, null);
  console.log("OK  JSON without verdict field returns null");
}

// 7. Findings list > 5 entries is capped to 5
{
  const findings = Array.from({ length: 8 }, (_, i) => ({
    severity: "NIT",
    file: `file${i}.js`,
    line: i + 1,
    why: `reason ${i}`,
  }));
  const payload = JSON.stringify({ verdict: "approve-ready", confidence: 2, summary: "Minor nits.", findings });
  const result = withStub(payload, () =>
    claudeReview({ diff: "diff text" })
  );
  assert.ok(result !== null);
  assert.equal(result.findings.length, 5, `expected 5, got ${result.findings.length}`);
  console.log("OK  findings array > 5 is capped to 5");
}

// 8. Unknown severity is normalized to "ISSUE"
{
  const payload = JSON.stringify({
    verdict: "approve-ready",
    confidence: 3,
    summary: "ok",
    findings: [{ severity: "WARNING", file: "x.js", line: 1, why: "some reason" }],
  });
  const result = withStub(payload, () =>
    claudeReview({ diff: "diff text" })
  );
  assert.ok(result !== null);
  assert.equal(result.findings[0].severity, "ISSUE");
  console.log("OK  unknown severity normalized to ISSUE");
}

// 9. Non-integer line is coerced to null
{
  const payload = JSON.stringify({
    verdict: "approve-ready",
    confidence: 3,
    summary: "ok",
    findings: [{ severity: "CRITICAL", file: "y.js", line: "not-a-number", why: "bad" }],
  });
  const result = withStub(payload, () =>
    claudeReview({ diff: "diff text" })
  );
  assert.ok(result !== null);
  assert.equal(result.findings[0].line, null);
  console.log("OK  non-integer line coerced to null");
}

// 10. Non-integer confidence is coerced to null
{
  const payload = JSON.stringify({
    verdict: "approve-ready",
    confidence: "high",
    summary: "ok",
    findings: [],
  });
  const result = withStub(payload, () =>
    claudeReview({ diff: "diff text" })
  );
  assert.ok(result !== null);
  assert.equal(result.confidence, null);
  console.log("OK  non-integer confidence coerced to null");
}

// 11. Diff > 40 000 chars causes truncation marker to appear in prompt.
//     Verified via CLAUDE_STDIN_CAPTURE env trick mirroring how claude-code-pass tests work.
{
  const stdinCapturePath = join(mkdtempSync(join(tmpdir(), "claude-review-cap-")), "stdin.txt");
  const work = mkdtempSync(join(tmpdir(), "claude-review-test-"));
  const binDir = join(work, "bin");
  mkdirSync(binDir);
  makeBin(
    binDir,
    "claude",
    `#!/usr/bin/env bash
if [ "$1" = "--version" ]; then echo "stub claude 1.0"; exit 0; fi
cat > "$CLAUDE_STDIN_CAPTURE"
printf '%s' '{"verdict":"approve-ready","confidence":1,"summary":"ok","findings":[]}'
`,
  );
  const oldPath = process.env.PATH;
  const oldCapture = process.env.CLAUDE_STDIN_CAPTURE;
  process.env.PATH = `${binDir}:${oldPath}`;
  process.env.CLAUDE_STDIN_CAPTURE = stdinCapturePath;
  const longDiff = "x".repeat(41_000);
  try {
    const result = claudeReview({ diff: longDiff });
    assert.ok(result !== null);
    const captured = readFileSync(stdinCapturePath, "utf8");
    assert.match(captured, /diff truncated for review/, "expected truncation marker in prompt");
  } finally {
    process.env.PATH = oldPath;
    if (oldCapture === undefined) delete process.env.CLAUDE_STDIN_CAPTURE;
    else process.env.CLAUDE_STDIN_CAPTURE = oldCapture;
    rmSync(work, { recursive: true, force: true });
    rmSync(stdinCapturePath, { force: true });
  }
  console.log("OK  diff > 40 000 chars triggers truncation marker in prompt");
}

// 12. findings entries missing a 'why' field are filtered out
{
  const payload = JSON.stringify({
    verdict: "approve-ready",
    confidence: 2,
    summary: "ok",
    findings: [
      { severity: "ISSUE", file: "a.js", line: 1 },         // no 'why' — should be dropped
      { severity: "NIT", file: "b.js", line: 2, why: "ok" }, // valid — kept
    ],
  });
  const result = withStub(payload, () =>
    claudeReview({ diff: "diff text" })
  );
  assert.ok(result !== null);
  assert.equal(result.findings.length, 1, "entry without 'why' should be filtered");
  assert.equal(result.findings[0].file, "b.js");
  console.log("OK  findings entries without 'why' are filtered out");
}

// 13. why string is truncated to 200 chars
{
  const longWhy = "a".repeat(250);
  const payload = JSON.stringify({
    verdict: "approve-ready",
    confidence: 3,
    summary: "ok",
    findings: [{ severity: "ISSUE", file: "c.js", line: 5, why: longWhy }],
  });
  const result = withStub(payload, () =>
    claudeReview({ diff: "diff text" })
  );
  assert.ok(result !== null);
  assert.equal(result.findings[0].why.length, 200);
  console.log("OK  finding 'why' truncated to 200 chars");
}

// 14. findings that is not an array → treated as empty array
{
  const payload = JSON.stringify({
    verdict: "approve-ready",
    confidence: 1,
    summary: "ok",
    findings: "should be an array",
  });
  const result = withStub(payload, () =>
    claudeReview({ diff: "diff text" })
  );
  assert.ok(result !== null);
  assert.deepEqual(result.findings, []);
  console.log("OK  non-array findings defaults to empty array");
}

console.log("\nAll claude-review tests passed.");
