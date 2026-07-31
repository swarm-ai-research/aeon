// claude-review.test.mjs — Tests for claudeReview's internal parseReview logic.
//
// Exercises edge-case branches in parseReview (private) via the exported
// claudeReview API, using fake `claude` binaries on PATH — same pattern
// as claude-code-pass.test.mjs.
//
// Run: node scripts/fleet-executors/claude-review.test.mjs

import { mkdtempSync, writeFileSync, chmodSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import assert from "node:assert/strict";
import { claudeReview } from "./claude-review.mjs";

// Install a fake `claude` binary at the front of PATH for the duration of fn().
// The stub:
//   - `--version` → exits 0 (signals "claude is available")
//   - everything else → prints $CLAUDE_STUB_OUT and exits 0
function withStub(fn) {
  const dir = mkdtempSync(join(tmpdir(), "cr-test-"));
  try {
    const bin = join(dir, "claude");
    writeFileSync(
      bin,
      `#!/usr/bin/env bash\nif [ "$1" = "--version" ]; then echo "stub"; exit 0; fi\nprintf '%s\\n' "$CLAUDE_STUB_OUT"\n`,
    );
    chmodSync(bin, 0o755);
    const oldPath = process.env.PATH;
    process.env.PATH = `${dir}:${oldPath}`;
    try {
      return fn();
    } finally {
      process.env.PATH = oldPath;
    }
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
}

// Install a fake `claude` binary whose `--version` always exits non-zero.
function withUnavailableStub(fn) {
  const dir = mkdtempSync(join(tmpdir(), "cr-unavail-"));
  try {
    const bin = join(dir, "claude");
    writeFileSync(bin, `#!/usr/bin/env bash\nexit 1\n`);
    chmodSync(bin, 0o755);
    const oldPath = process.env.PATH;
    process.env.PATH = `${dir}:${oldPath}`;
    try {
      return fn();
    } finally {
      process.env.PATH = oldPath;
    }
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
}

// Install a fake `claude` that exits 0 for --version but non-zero for the
// actual review call.
function withCallFailStub(fn) {
  const dir = mkdtempSync(join(tmpdir(), "cr-callfail-"));
  try {
    const bin = join(dir, "claude");
    writeFileSync(
      bin,
      `#!/usr/bin/env bash\nif [ "$1" = "--version" ]; then echo "stub"; exit 0; fi\nexit 2\n`,
    );
    chmodSync(bin, 0o755);
    const oldPath = process.env.PATH;
    process.env.PATH = `${dir}:${oldPath}`;
    try {
      return fn();
    } finally {
      process.env.PATH = oldPath;
    }
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
}

// Set CLAUDE_STUB_OUT, call fn, then restore.
function withOutput(json, fn) {
  const prev = process.env.CLAUDE_STUB_OUT;
  process.env.CLAUDE_STUB_OUT = json;
  try {
    return fn();
  } finally {
    if (prev === undefined) delete process.env.CLAUDE_STUB_OUT;
    else process.env.CLAUDE_STUB_OUT = prev;
  }
}

const SAMPLE_DIFF = "--- a/foo.mjs\n+++ b/foo.mjs\n@@ -1 +1 @@\n+const x = 1;\n";

const VALID_REVIEW = JSON.stringify({
  verdict: "approve-ready",
  confidence: 4,
  summary: "Looks good",
  findings: [{ severity: "ISSUE", file: "foo.mjs", line: 12, why: "side effect" }],
});

// 1. Empty diff → null immediately (no binary needed).
{
  const result = claudeReview({ diff: "" });
  assert.equal(result, null);
  console.log("OK  empty diff → null without invoking claude");
}

// 2. claude --version fails → null.
{
  const result = withUnavailableStub(() => claudeReview({ diff: SAMPLE_DIFF }));
  assert.equal(result, null);
  console.log("OK  claude --version fails → null");
}

// 3. claude review call exits non-zero → null.
{
  const result = withCallFailStub(() => claudeReview({ diff: SAMPLE_DIFF }));
  assert.equal(result, null);
  console.log("OK  claude review call exits non-zero → null");
}

// 4. Valid JSON → structured result with all fields populated.
{
  const result = withStub(() => withOutput(VALID_REVIEW, () => claudeReview({ diff: SAMPLE_DIFF })));
  assert.notEqual(result, null);
  assert.equal(result.verdict, "approve-ready");
  assert.equal(result.confidence, 4);
  assert.equal(result.summary, "Looks good");
  assert.equal(result.findings.length, 1);
  assert.equal(result.findings[0].line, 12);
  assert.equal(result.findings[0].severity, "ISSUE");
  console.log("OK  valid JSON → structured result");
}

// 5. JSON embedded in leading prose — parseReview's start/end scan extracts it.
{
  const prose = `Sure, here is the review:\n${VALID_REVIEW}\nThat is all.`;
  const result = withStub(() => withOutput(prose, () => claudeReview({ diff: SAMPLE_DIFF })));
  assert.notEqual(result, null);
  assert.equal(result.verdict, "approve-ready");
  console.log("OK  JSON embedded in prose → extracted via start/end scan");
}

// 6. Malformed JSON (no closing brace) → null.
{
  const result = withStub(() => withOutput("{not valid json", () => claudeReview({ diff: SAMPLE_DIFF })));
  assert.equal(result, null);
  console.log("OK  malformed JSON → null");
}

// 7. JSON.parse("null") — obj is null → null.
{
  const result = withStub(() => withOutput("null", () => claudeReview({ diff: SAMPLE_DIFF })));
  assert.equal(result, null);
  console.log("OK  JSON.parse(null) → null obj → null");
}

// 8. Verdict field missing → null.
{
  const noVerdict = JSON.stringify({ confidence: 3, findings: [] });
  const result = withStub(() => withOutput(noVerdict, () => claudeReview({ diff: SAMPLE_DIFF })));
  assert.equal(result, null);
  console.log("OK  missing verdict → null");
}

// 9. Unknown severity string → normalized to "ISSUE".
{
  const badSeverity = JSON.stringify({
    verdict: "discussion-needed",
    confidence: 2,
    summary: "needs work",
    findings: [{ severity: "WARNING", file: "x.mjs", line: 5, why: "possible issue" }],
  });
  const result = withStub(() => withOutput(badSeverity, () => claudeReview({ diff: SAMPLE_DIFF })));
  assert.notEqual(result, null);
  assert.equal(result.findings[0].severity, "ISSUE");
  console.log("OK  unknown severity 'WARNING' → normalized to 'ISSUE'");
}

// 10. Non-integer line (string "42") → line: null.
{
  const strLine = JSON.stringify({
    verdict: "approve-ready",
    confidence: 5,
    summary: "ok",
    findings: [{ severity: "NIT", file: "y.mjs", line: "42", why: "style nit" }],
  });
  const result = withStub(() => withOutput(strLine, () => claudeReview({ diff: SAMPLE_DIFF })));
  assert.notEqual(result, null);
  assert.equal(result.findings[0].line, null);
  console.log("OK  non-integer line ('42') → null");
}

// 11. More than 5 findings → sliced to exactly 5.
{
  const manyFindings = JSON.stringify({
    verdict: "blocked: too many issues",
    confidence: 1,
    summary: "lots of issues",
    findings: Array.from({ length: 8 }, (_, i) => ({
      severity: "ISSUE",
      file: `f${i}.mjs`,
      line: i + 1,
      why: `issue ${i}`,
    })),
  });
  const result = withStub(() => withOutput(manyFindings, () => claudeReview({ diff: SAMPLE_DIFF })));
  assert.notEqual(result, null);
  assert.equal(result.findings.length, 5);
  console.log("OK  8 findings → sliced to 5");
}

// 12. Non-array findings (object) → treated as empty array.
{
  const objFindings = JSON.stringify({
    verdict: "approve-ready",
    confidence: 4,
    summary: "ok",
    findings: { issue: "should be an array" },
  });
  const result = withStub(() => withOutput(objFindings, () => claudeReview({ diff: SAMPLE_DIFF })));
  assert.notEqual(result, null);
  assert.equal(result.findings.length, 0);
  console.log("OK  non-array findings → empty array");
}

// 13. Non-integer confidence (null) → confidence: null in result.
{
  const nullConf = JSON.stringify({
    verdict: "discussion-needed",
    confidence: null,
    summary: "uncertain",
    findings: [],
  });
  const result = withStub(() => withOutput(nullConf, () => claudeReview({ diff: SAMPLE_DIFF })));
  assert.notEqual(result, null);
  assert.equal(result.confidence, null);
  console.log("OK  null confidence → confidence: null");
}

// 14. diff longer than MAX_DIFF_CHARS (40 000) → still returns a result (truncation
//     is an internal concern; the function should not crash or return null).
{
  const longDiff = "+" + "x".repeat(41000);
  const result = withStub(() => withOutput(VALID_REVIEW, () => claudeReview({ diff: longDiff })));
  assert.notEqual(result, null);
  assert.equal(result.verdict, "approve-ready");
  console.log("OK  diff > MAX_DIFF_CHARS → truncated internally, result still returned");
}

console.log("\nAll claude-review tests passed.");
