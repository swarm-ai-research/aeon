// claude-review.test.mjs — Tests for claudeReview / parseReview branches.
//
// Exercises the parseReview branches that are unreachable through the happy
// path: malformed output, severity normalization, findings cap, confidence
// coercion, diff truncation, and CLI-unavailable fallback.
//
// Run: node scripts/fleet-executors/claude-review.test.mjs

import { mkdtempSync, writeFileSync, rmSync, chmodSync, mkdirSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import assert from "node:assert/strict";
import { claudeReview } from "./claude-review.mjs";

function makeBin(dir, name, script) {
  const p = join(dir, name);
  writeFileSync(p, script);
  chmodSync(p, 0o755);
  return p;
}

function withPath(binDir, fn) {
  const old = process.env.PATH;
  process.env.PATH = `${binDir}:${old}`;
  try { return fn(); } finally { process.env.PATH = old; }
}

// Build a stub claude that echoes a fixed stdout payload after passing the
// --version check.
function stubClaude(dir, payload) {
  return makeBin(dir, "claude", `#!/usr/bin/env bash
if [ "$1" = "--version" ]; then echo "stub claude 1.0"; exit 0; fi
printf '%s' ${JSON.stringify(payload)}
`);
}

// 1. null diff → returns null immediately (no claude invocation needed).
{
  const bin = mkdtempSync(join(tmpdir(), "cr-test-"));
  try {
    makeBin(bin, "claude", `#!/usr/bin/env bash\necho "should not be called" >&2\nexit 99\n`);
    const result = withPath(bin, () => claudeReview({ diff: "", repoDir: bin }));
    assert.equal(result, null, "empty diff should return null without calling claude");
    const result2 = withPath(bin, () => claudeReview({ diff: null, repoDir: bin }));
    assert.equal(result2, null, "null diff should return null");
  } finally { rmSync(bin, { recursive: true, force: true }); }
  console.log("OK  null/empty diff → null without claude invocation");
}

// 2. claude --version exits non-zero → returns null (CLI unavailable path).
{
  const bin = mkdtempSync(join(tmpdir(), "cr-test-"));
  makeBin(bin, "claude", `#!/usr/bin/env bash\nexit 1\n`);
  try {
    const result = withPath(bin, () => claudeReview({ diff: "- old\n+ new\n", repoDir: bin }));
    assert.equal(result, null, "unavailable CLI should return null");
  } finally { rmSync(bin, { recursive: true, force: true }); }
  console.log("OK  claude --version failure → null");
}

// 3. claude returns empty stdout → returns null (proc.stdout falsy path).
{
  const bin = mkdtempSync(join(tmpdir(), "cr-test-"));
  makeBin(bin, "claude", `#!/usr/bin/env bash\nif [ "$1" = "--version" ]; then echo "stub"; exit 0; fi\nexit 0\n`);
  try {
    const result = withPath(bin, () => claudeReview({ diff: "- old\n+ new\n", repoDir: bin }));
    assert.equal(result, null, "empty stdout should return null");
  } finally { rmSync(bin, { recursive: true, force: true }); }
  console.log("OK  empty claude stdout → null (proc.stdout falsy branch)");
}

// 4. claude exits non-zero with output → null (status !== 0 branch).
{
  const bin = mkdtempSync(join(tmpdir(), "cr-test-"));
  makeBin(bin, "claude", `#!/usr/bin/env bash\nif [ "$1" = "--version" ]; then echo "stub"; exit 0; fi\necho "some output"\nexit 1\n`);
  try {
    const result = withPath(bin, () => claudeReview({ diff: "- a\n+ b\n", repoDir: bin }));
    assert.equal(result, null, "non-zero exit should return null");
  } finally { rmSync(bin, { recursive: true, force: true }); }
  console.log("OK  claude non-zero exit → null");
}

// 5. parseReview: output with no JSON delimiters → null.
{
  const bin = mkdtempSync(join(tmpdir(), "cr-test-"));
  stubClaude(bin, "no braces here at all");
  try {
    const result = withPath(bin, () => claudeReview({ diff: "- a\n+ b\n", repoDir: bin }));
    assert.equal(result, null, "no-brace output should return null");
  } finally { rmSync(bin, { recursive: true, force: true }); }
  console.log("OK  parseReview: no JSON delimiters → null");
}

// 6. parseReview: malformed JSON between braces → null (JSON.parse throws).
{
  const bin = mkdtempSync(join(tmpdir(), "cr-test-"));
  stubClaude(bin, "{ this is not valid json }");
  try {
    const result = withPath(bin, () => claudeReview({ diff: "- a\n+ b\n", repoDir: bin }));
    assert.equal(result, null, "invalid JSON should return null");
  } finally { rmSync(bin, { recursive: true, force: true }); }
  console.log("OK  parseReview: malformed JSON → null");
}

// 7. parseReview: valid JSON but verdict is missing → null.
{
  const bin = mkdtempSync(join(tmpdir(), "cr-test-"));
  stubClaude(bin, JSON.stringify({ confidence: 3, findings: [] }));
  try {
    const result = withPath(bin, () => claudeReview({ diff: "- a\n+ b\n", repoDir: bin }));
    assert.equal(result, null, "missing verdict should return null");
  } finally { rmSync(bin, { recursive: true, force: true }); }
  console.log("OK  parseReview: valid JSON, verdict missing → null");
}

// 8. parseReview: verdict is non-string (e.g. a number) → null.
{
  const bin = mkdtempSync(join(tmpdir(), "cr-test-"));
  stubClaude(bin, JSON.stringify({ verdict: 42, findings: [] }));
  try {
    const result = withPath(bin, () => claudeReview({ diff: "- a\n+ b\n", repoDir: bin }));
    assert.equal(result, null, "non-string verdict should return null");
  } finally { rmSync(bin, { recursive: true, force: true }); }
  console.log("OK  parseReview: non-string verdict → null");
}

// 9. parseReview: findings is not an array → treated as empty array.
{
  const bin = mkdtempSync(join(tmpdir(), "cr-test-"));
  stubClaude(bin, JSON.stringify({ verdict: "approve-ready", findings: "not an array", confidence: 4 }));
  try {
    const result = withPath(bin, () => claudeReview({ diff: "- a\n+ b\n", repoDir: bin }));
    assert.notEqual(result, null);
    assert.deepEqual(result.findings, [], "non-array findings should become empty array");
    assert.equal(result.verdict, "approve-ready");
  } finally { rmSync(bin, { recursive: true, force: true }); }
  console.log("OK  parseReview: non-array findings → empty array");
}

// 10. parseReview: unknown severity → normalised to 'ISSUE'.
{
  const bin = mkdtempSync(join(tmpdir(), "cr-test-"));
  const payload = JSON.stringify({
    verdict: "discussion-needed",
    confidence: 2,
    findings: [{ severity: "WARNING", file: "foo.js", line: 10, why: "something bad" }],
  });
  stubClaude(bin, payload);
  try {
    const result = withPath(bin, () => claudeReview({ diff: "- a\n+ b\n", repoDir: bin }));
    assert.notEqual(result, null);
    assert.equal(result.findings.length, 1);
    assert.equal(result.findings[0].severity, "ISSUE", "unknown severity should normalise to ISSUE");
  } finally { rmSync(bin, { recursive: true, force: true }); }
  console.log("OK  parseReview: unknown severity → 'ISSUE'");
}

// 11. parseReview: more than 5 findings → sliced to 5.
{
  const bin = mkdtempSync(join(tmpdir(), "cr-test-"));
  const findings = Array.from({ length: 8 }, (_, i) => ({
    severity: "NIT",
    file: `f${i}.js`,
    line: i + 1,
    why: `issue ${i}`,
  }));
  stubClaude(bin, JSON.stringify({ verdict: "approve-ready", confidence: 5, findings }));
  try {
    const result = withPath(bin, () => claudeReview({ diff: "- a\n+ b\n", repoDir: bin }));
    assert.notEqual(result, null);
    assert.equal(result.findings.length, 5, "findings should be capped at 5");
  } finally { rmSync(bin, { recursive: true, force: true }); }
  console.log("OK  parseReview: >5 findings → sliced to 5");
}

// 12. parseReview: `why` field > 200 chars → truncated to 200.
{
  const bin = mkdtempSync(join(tmpdir(), "cr-test-"));
  const longWhy = "x".repeat(250);
  stubClaude(bin, JSON.stringify({
    verdict: "approve-ready",
    confidence: 3,
    findings: [{ severity: "ISSUE", file: "a.js", line: 1, why: longWhy }],
  }));
  try {
    const result = withPath(bin, () => claudeReview({ diff: "- a\n+ b\n", repoDir: bin }));
    assert.notEqual(result, null);
    assert.equal(result.findings[0].why.length, 200, "why should be truncated to 200 chars");
  } finally { rmSync(bin, { recursive: true, force: true }); }
  console.log("OK  parseReview: long 'why' → truncated to 200");
}

// 13. parseReview: non-integer confidence → null in result.
{
  const bin = mkdtempSync(join(tmpdir(), "cr-test-"));
  stubClaude(bin, JSON.stringify({ verdict: "approve-ready", confidence: 3.7, findings: [] }));
  try {
    const result = withPath(bin, () => claudeReview({ diff: "- a\n+ b\n", repoDir: bin }));
    assert.notEqual(result, null);
    assert.equal(result.confidence, null, "float confidence should become null");
  } finally { rmSync(bin, { recursive: true, force: true }); }
  console.log("OK  parseReview: float confidence → null");
}

// 14. parseReview: missing confidence → null in result.
{
  const bin = mkdtempSync(join(tmpdir(), "cr-test-"));
  stubClaude(bin, JSON.stringify({ verdict: "blocked: no tests", findings: [] }));
  try {
    const result = withPath(bin, () => claudeReview({ diff: "- a\n+ b\n", repoDir: bin }));
    assert.notEqual(result, null);
    assert.equal(result.confidence, null, "missing confidence should be null");
    assert.equal(result.verdict, "blocked: no tests");
  } finally { rmSync(bin, { recursive: true, force: true }); }
  console.log("OK  parseReview: missing confidence → null");
}

// 15. parseReview: finding with non-integer line → null line in result.
{
  const bin = mkdtempSync(join(tmpdir(), "cr-test-"));
  stubClaude(bin, JSON.stringify({
    verdict: "approve-ready",
    confidence: 4,
    findings: [{ severity: "CRITICAL", file: "b.ts", line: "not-a-number", why: "bad thing" }],
  }));
  try {
    const result = withPath(bin, () => claudeReview({ diff: "- a\n+ b\n", repoDir: bin }));
    assert.notEqual(result, null);
    assert.equal(result.findings[0].line, null, "non-integer line should become null");
  } finally { rmSync(bin, { recursive: true, force: true }); }
  console.log("OK  parseReview: non-integer line → null");
}

// 16. buildPrompt diff truncation: diff > 40000 chars gets the ellipsis trailer.
//     Captured by writing the claude stdin to a temp file.
{
  const bin = mkdtempSync(join(tmpdir(), "cr-test-"));
  const stdinFile = join(bin, "stdin.txt");
  makeBin(bin, "claude", `#!/usr/bin/env bash
if [ "$1" = "--version" ]; then echo "stub"; exit 0; fi
cat > ${JSON.stringify(stdinFile)}
echo '{"verdict":"approve-ready","confidence":5,"findings":[]}'
`);
  try {
    const longDiff = "+" + "a".repeat(40001);
    withPath(bin, () => claudeReview({ diff: longDiff, repoDir: bin }));
    const captured = (await import("node:fs")).readFileSync(stdinFile, "utf8");
    assert.match(captured, /\[diff truncated for review\]/, "long diff should include truncation marker");
    assert.ok(!captured.includes("a".repeat(40002)), "truncated diff must not include chars past the 40000 limit");
  } finally { rmSync(bin, { recursive: true, force: true }); }
  console.log("OK  buildPrompt: diff > 40000 chars → truncated with ellipsis trailer");
}

// 17. parseReview: finding without 'why' string is filtered out.
{
  const bin = mkdtempSync(join(tmpdir(), "cr-test-"));
  stubClaude(bin, JSON.stringify({
    verdict: "approve-ready",
    confidence: 5,
    findings: [
      { severity: "ISSUE", file: "a.js", line: 1, why: "real finding" },
      { severity: "NIT", file: "b.js", line: 2 },           // missing 'why' → filtered
      { severity: "CRITICAL", file: "c.js", line: 3, why: 42 }, // why is not string → filtered
    ],
  }));
  try {
    const result = withPath(bin, () => claudeReview({ diff: "- a\n+ b\n", repoDir: bin }));
    assert.notEqual(result, null);
    assert.equal(result.findings.length, 1, "findings missing 'why' string should be filtered out");
    assert.equal(result.findings[0].why, "real finding");
  } finally { rmSync(bin, { recursive: true, force: true }); }
  console.log("OK  parseReview: findings without 'why' string → filtered out");
}

// 18. parseReview: JSON embedded in prose (extra text around the braces).
{
  const bin = mkdtempSync(join(tmpdir(), "cr-test-"));
  const json = JSON.stringify({ verdict: "approve-ready", confidence: 5, findings: [] });
  stubClaude(bin, `Here is my review:\n${json}\nThat's all.`);
  try {
    const result = withPath(bin, () => claudeReview({ diff: "- a\n+ b\n", repoDir: bin }));
    assert.notEqual(result, null, "JSON embedded in prose should still parse");
    assert.equal(result.verdict, "approve-ready");
  } finally { rmSync(bin, { recursive: true, force: true }); }
  console.log("OK  parseReview: JSON embedded in prose → extracted and parsed");
}

// 19. summary field missing → empty string default.
{
  const bin = mkdtempSync(join(tmpdir(), "cr-test-"));
  stubClaude(bin, JSON.stringify({ verdict: "approve-ready", confidence: 1, findings: [] }));
  try {
    const result = withPath(bin, () => claudeReview({ diff: "- a\n+ b\n", repoDir: bin }));
    assert.notEqual(result, null);
    assert.equal(result.summary, "", "missing summary should default to empty string");
  } finally { rmSync(bin, { recursive: true, force: true }); }
  console.log("OK  parseReview: missing summary → empty string");
}

// 20. summary field is non-string → empty string default.
{
  const bin = mkdtempSync(join(tmpdir(), "cr-test-"));
  stubClaude(bin, JSON.stringify({ verdict: "approve-ready", confidence: 2, summary: 99, findings: [] }));
  try {
    const result = withPath(bin, () => claudeReview({ diff: "- a\n+ b\n", repoDir: bin }));
    assert.notEqual(result, null);
    assert.equal(result.summary, "", "non-string summary should default to empty string");
  } finally { rmSync(bin, { recursive: true, force: true }); }
  console.log("OK  parseReview: non-string summary → empty string");
}

console.log("\nAll claude-review tests passed.");
