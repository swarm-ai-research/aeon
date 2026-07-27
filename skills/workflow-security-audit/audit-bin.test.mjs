// audit-bin.test.mjs — Validates pre-cached binaries in .audit-bin/.
//
// The workflow-security-audit skill bootstraps zizmor and actionlint from
// .audit-bin/ before falling back to network installs.  If a binary loses
// its execute bit or is truncated the skill silently degrades to curl/pipx,
// which can be blocked in the GitHub Actions sandbox.
//
// These tests cover the two branches in SKILL.md step 0b:
//   [ -x ".audit-bin/zizmor" ]    → use cached binary (happy path)
//   [ -x ".audit-bin/actionlint" ] → use cached binary (happy path)
// and flag regressions before they cause a silent WORKFLOW_AUDIT_TOOL_FAIL.
//
// Run: node skills/workflow-security-audit/audit-bin.test.mjs

import { accessSync, constants, readFileSync, statSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import assert from "node:assert/strict";

const HERE = dirname(fileURLToPath(import.meta.url));
const REPO_ROOT = join(HERE, "..", "..");
const AUDIT_BIN = join(REPO_ROOT, ".audit-bin");
const SKILL_MD = join(HERE, "SKILL.md");

// ELF magic bytes: the first 4 bytes of any Linux ELF binary
const ELF_MAGIC = [0x7f, 0x45, 0x4c, 0x46]; // \x7fELF

let passed = 0;
let failed = 0;

function test(label, fn) {
  try {
    fn();
    passed++;
    console.log(`  ✓ ${label}`);
  } catch (e) {
    failed++;
    console.error(`  ✗ ${label}: ${e.message}`);
  }
}

// ── zizmor ───────────────────────────────────────────────────────────────────

console.log("zizmor:");
{
  const bin = join(AUDIT_BIN, "zizmor");

  test("binary exists", () => {
    assert.ok(statSync(bin).isFile(), "zizmor should be a regular file");
  });

  test("binary is non-empty (not a truncated download)", () => {
    assert.ok(statSync(bin).size > 0, `zizmor is 0 bytes`);
  });

  test("binary has ELF magic (is an executable, not a shell stub or empty file)", () => {
    const buf = readFileSync(bin);
    for (let i = 0; i < ELF_MAGIC.length; i++) {
      assert.equal(buf[i], ELF_MAGIC[i],
        `byte ${i} is 0x${buf[i]?.toString(16)} — expected 0x${ELF_MAGIC[i].toString(16)}`);
    }
  });

  test("binary is executable (the [ -x ] check in SKILL.md 0b passes)", () => {
    // The bootstrap logic is: if [ -x ".audit-bin/zizmor" ]; then use it.
    // If this bit is missing the skill falls back to pipx/pip installs,
    // which the GitHub Actions sandbox may block.
    accessSync(bin, constants.X_OK);
  });
}

// ── actionlint ───────────────────────────────────────────────────────────────

console.log("\nactionlint:");
{
  const bin = join(AUDIT_BIN, "actionlint");

  test("binary exists", () => {
    assert.ok(statSync(bin).isFile(), "actionlint should be a regular file");
  });

  test("binary is non-empty (not a truncated download)", () => {
    assert.ok(statSync(bin).size > 0, `actionlint is 0 bytes`);
  });

  test("binary has ELF magic (is an executable, not a shell stub or empty file)", () => {
    const buf = readFileSync(bin);
    for (let i = 0; i < ELF_MAGIC.length; i++) {
      assert.equal(buf[i], ELF_MAGIC[i],
        `byte ${i} is 0x${buf[i]?.toString(16)} — expected 0x${ELF_MAGIC[i].toString(16)}`);
    }
  });

  test("binary is executable (the [ -x ] check in SKILL.md 0b passes)", () => {
    accessSync(bin, constants.X_OK);
  });
}

// ── actionlint.tar.gz ────────────────────────────────────────────────────────

console.log("\nactionlint.tar.gz:");
{
  const archive = join(AUDIT_BIN, "actionlint.tar.gz");

  test("archive exists", () => {
    assert.ok(statSync(archive).isFile(), "actionlint.tar.gz should be a regular file");
  });

  test("archive is non-empty", () => {
    assert.ok(statSync(archive).size > 0, "actionlint.tar.gz is 0 bytes");
  });

  test("archive has gzip magic bytes (0x1f 0x8b)", () => {
    const buf = readFileSync(archive);
    assert.equal(buf[0], 0x1f, `byte 0 is 0x${buf[0]?.toString(16)} — expected 0x1f`);
    assert.equal(buf[1], 0x8b, `byte 1 is 0x${buf[1]?.toString(16)} — expected 0x8b`);
  });
}

// ── SKILL.md version pin ─────────────────────────────────────────────────────

console.log("\nSKILL.md version pin:");
{
  const skill = readFileSync(SKILL_MD, "utf8");

  test("ZIZMOR_VERSION pin present in SKILL.md", () => {
    assert.match(skill, /ZIZMOR_VERSION="[^"]+"/,
      "ZIZMOR_VERSION assignment not found — was it removed from step 0b?");
  });

  test("ZIZMOR_VERSION has semver format", () => {
    const m = skill.match(/ZIZMOR_VERSION="([^"]+)"/);
    assert.ok(m, "ZIZMOR_VERSION not found");
    assert.match(m[1], /^\d+\.\d+\.\d+$/,
      `ZIZMOR_VERSION "${m[1]}" does not look like a semver string`);
  });
}

// ── Results ──────────────────────────────────────────────────────────────────

console.log(`\n${passed} passed, ${failed} failed`);
if (failed > 0) throw new Error(`${failed} test(s) failed`);
