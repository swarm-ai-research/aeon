// audit-bin.test.mjs — Smoke tests for the committed .audit-bin/ executables.
//
// Verifies that the pre-built actionlint and zizmor binaries are present,
// carry the executable bit, are structurally valid, and that the zizmor
// version pinned in SKILL.md matches the binary that was actually committed.
//
// Catches: accidental deletion, chmod regressions, tarball corruption,
// and version drift between the SKILL.md pin and the committed binary.
//
// Run: node scripts/audit-bin.test.mjs

import { existsSync, accessSync, constants, readFileSync } from "node:fs";
import { spawnSync } from "node:child_process";
import { join } from "node:path";
import assert from "node:assert/strict";

const REPO_ROOT = new URL("../", import.meta.url).pathname;
const AUDIT_BIN = join(REPO_ROOT, ".audit-bin");
const SKILL_MD = join(REPO_ROOT, "skills/workflow-security-audit/SKILL.md");

let passed = 0;
let failed = 0;

function test(label, fn) {
  try {
    fn();
    passed++;
    console.log(`OK  ${label}`);
  } catch (err) {
    failed++;
    console.error(`FAIL ${label}\n     ${err.message}`);
  }
}

// 1. All three artefacts must exist.
test("zizmor binary exists", () => {
  assert.ok(existsSync(join(AUDIT_BIN, "zizmor")), ".audit-bin/zizmor not found");
});
test("actionlint binary exists", () => {
  assert.ok(existsSync(join(AUDIT_BIN, "actionlint")), ".audit-bin/actionlint not found");
});
test("actionlint.tar.gz exists", () => {
  assert.ok(
    existsSync(join(AUDIT_BIN, "actionlint.tar.gz")),
    ".audit-bin/actionlint.tar.gz not found",
  );
});

// 2. Both executables must have the executable bit set (the SKILL.md bootstrap
//    uses `[ -x ".audit-bin/zizmor" ]` / `[ -x ".audit-bin/actionlint" ]`).
test("zizmor is executable (X_OK)", () => {
  accessSync(join(AUDIT_BIN, "zizmor"), constants.X_OK);
});
test("actionlint is executable (X_OK)", () => {
  accessSync(join(AUDIT_BIN, "actionlint"), constants.X_OK);
});

// 3. actionlint.tar.gz must be a valid gzip stream.  The gzip magic is the
//    two-byte sequence 0x1f 0x8b; a corrupted upload produces a file whose
//    first bytes are HTML or zeros instead.
test("actionlint.tar.gz starts with gzip magic bytes (0x1f 0x8b)", () => {
  const buf = readFileSync(join(AUDIT_BIN, "actionlint.tar.gz"));
  assert.equal(buf[0], 0x1f, `expected 0x1f at offset 0, got 0x${buf[0].toString(16)}`);
  assert.equal(buf[1], 0x8b, `expected 0x8b at offset 1, got 0x${buf[1].toString(16)}`);
});

// 4. SKILL.md version pin must be present, and the committed zizmor binary
//    must embed the same version string.  zizmor is a Rust binary whose version
//    string is baked into the ELF binary; reading it as bytes avoids any need
//    to execute the binary (which may fail on sandboxed or cross-arch runners).
test("SKILL.md contains a ZIZMOR_VERSION pin", () => {
  const md = readFileSync(SKILL_MD, "utf8");
  assert.match(
    md,
    /ZIZMOR_VERSION="[\d.]+"/,
    'SKILL.md must contain ZIZMOR_VERSION="<semver>"',
  );
});

test("committed zizmor binary embeds the SKILL.md ZIZMOR_VERSION string", () => {
  const md = readFileSync(SKILL_MD, "utf8");
  const m = md.match(/ZIZMOR_VERSION="([\d.]+)"/);
  assert.ok(m, 'SKILL.md must contain ZIZMOR_VERSION="<semver>"');
  const pinned = m[1]; // e.g. "1.25.2"

  // Read the binary as a buffer and search for the version string.  The Rust
  // toolchain embeds the crate version inside the ELF binary as a UTF-8 string,
  // so a simple byte-scan reliably finds it without executing the binary.
  const binary = readFileSync(join(AUDIT_BIN, "zizmor"));
  const needle = Buffer.from(pinned, "utf8");
  let found = false;
  for (let i = 0; i <= binary.length - needle.length; i++) {
    if (binary.subarray(i, i + needle.length).equals(needle)) {
      found = true;
      break;
    }
  }
  assert.ok(
    found,
    `version string "${pinned}" not found in .audit-bin/zizmor — ` +
      "binary may be out of sync with the SKILL.md pin; update one or the other",
  );
});

// 5. Edge case: both binaries must be non-empty (a zero-byte file would pass
//    the existence check but is clearly corrupt).
test("zizmor binary is non-empty", () => {
  const buf = readFileSync(join(AUDIT_BIN, "zizmor"));
  assert.ok(buf.length > 0, ".audit-bin/zizmor is empty");
});
test("actionlint binary is non-empty", () => {
  const buf = readFileSync(join(AUDIT_BIN, "actionlint"));
  assert.ok(buf.length > 0, ".audit-bin/actionlint is empty");
});

// 6. If the binaries can be executed on this platform, verify that their
//    --version flag exits 0 and returns a semver-shaped string.  If execution
//    fails (wrong arch, sandbox, missing dynamic linker) we skip gracefully.
function tryRunVersion(binary) {
  const r = spawnSync(binary, ["--version"], { encoding: "utf8", timeout: 5000 });
  if (r.error || r.status === null) return null; // execution not possible
  return { status: r.status, output: (r.stdout + r.stderr).trim() };
}

test("zizmor --version exits 0 and emits a semver string (skipped if not executable here)", () => {
  const r = tryRunVersion(join(AUDIT_BIN, "zizmor"));
  if (r === null) {
    console.log("     (skipped — binary not runnable on this platform)");
    return;
  }
  assert.equal(r.status, 0, `zizmor --version exited ${r.status}`);
  assert.match(r.output, /\d+\.\d+\.\d+/, `unexpected --version output: "${r.output}"`);
});

test("actionlint --version exits 0 and emits a semver string (skipped if not executable here)", () => {
  const r = tryRunVersion(join(AUDIT_BIN, "actionlint"));
  if (r === null) {
    console.log("     (skipped — binary not runnable on this platform)");
    return;
  }
  assert.equal(r.status, 0, `actionlint --version exited ${r.status}`);
  assert.match(r.output, /\d+\.\d+\.\d+/, `unexpected --version output: "${r.output}"`);
});

// ── Summary ─────────────────────────────────────────────────────────────────
if (failed > 0) {
  console.error(`\n${failed} test(s) failed, ${passed} passed.`);
  process.exit(1);
}
console.log(`\nAll ${passed} audit-bin tests passed.`);
