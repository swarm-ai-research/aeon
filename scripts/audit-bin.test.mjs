// audit-bin.test.mjs — Structural tests for the pre-built scanner binaries in .audit-bin/
//
// The workflow-security-audit skill relies on .audit-bin/zizmor and
// .audit-bin/actionlint being executable before falling back to pip/pipx or
// curl installs. If a binary exists but lacks the execute bit (e.g. after a
// git commit without filemode tracking), the SKILL.md `[ -x ... ]` check
// silently fails, and the skill tries a network install that the Actions
// sandbox may block — yielding WORKFLOW_AUDIT_TOOL_FAIL on every run.
//
// These tests catch that class of failure without executing the binaries
// (keeping the tests sandbox-safe and platform-independent).
//
// Run: node scripts/audit-bin.test.mjs

import { statSync, existsSync, readFileSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { spawnSync } from "node:child_process";
import { mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import assert from "node:assert/strict";

const REPO_ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");
const AUDIT_BIN = join(REPO_ROOT, ".audit-bin");

const ACTIONLINT     = join(AUDIT_BIN, "actionlint");
const ACTIONLINT_TAR = join(AUDIT_BIN, "actionlint.tar.gz");
const ZIZMOR         = join(AUDIT_BIN, "zizmor");

// Returns true if any execute bit is set (owner/group/other).
function isExecutable(mode) {
  return (mode & 0o111) !== 0;
}

// 1. .audit-bin/actionlint exists and is executable.
//    If it exists but is not executable, `[ -x .audit-bin/actionlint ]` in
//    SKILL.md returns false, triggering the curl-installer fallback which may
//    be blocked in the GitHub Actions sandbox.
{
  assert.ok(existsSync(ACTIONLINT), ".audit-bin/actionlint must exist");
  const stat = statSync(ACTIONLINT);
  assert.ok(stat.isFile(), ".audit-bin/actionlint must be a regular file, not a symlink or directory");
  assert.ok(
    isExecutable(stat.mode),
    `.audit-bin/actionlint must have execute permission (mode: ${stat.mode.toString(8)}). ` +
    "Ensure the file is committed with 'git add --chmod=+x .audit-bin/actionlint'."
  );
  console.log("OK  .audit-bin/actionlint exists and is executable");
}

// 2. .audit-bin/zizmor exists and is executable.
//    Same reasoning — non-executable zizmor causes the pipx/pip fallback path
//    in SKILL.md step 0b to run instead of using the committed binary.
{
  assert.ok(existsSync(ZIZMOR), ".audit-bin/zizmor must exist");
  const stat = statSync(ZIZMOR);
  assert.ok(stat.isFile(), ".audit-bin/zizmor must be a regular file, not a symlink or directory");
  assert.ok(
    isExecutable(stat.mode),
    `.audit-bin/zizmor must have execute permission (mode: ${stat.mode.toString(8)}). ` +
    "Ensure the file is committed with 'git add --chmod=+x .audit-bin/zizmor'."
  );
  console.log("OK  .audit-bin/zizmor exists and is executable");
}

// 3. actionlint.tar.gz exists and is non-empty.
//    The tarball is used as a recovery artifact when the loose binary is
//    missing or to reinstall on a fresh machine.
{
  assert.ok(existsSync(ACTIONLINT_TAR), ".audit-bin/actionlint.tar.gz must exist");
  const stat = statSync(ACTIONLINT_TAR);
  assert.ok(stat.isFile(), ".audit-bin/actionlint.tar.gz must be a regular file");
  assert.ok(stat.size > 0, ".audit-bin/actionlint.tar.gz must not be empty (file is 0 bytes)");
  console.log(`OK  .audit-bin/actionlint.tar.gz exists (${stat.size} bytes)`);
}

// 4. actionlint.tar.gz is a structurally valid gzip+tar archive.
//    A corrupt archive would fail silently at install time, producing a
//    missing-binary state identical to a network-blocked pip install.
{
  const r = spawnSync("tar", ["-tzf", ACTIONLINT_TAR], { encoding: "utf8" });
  assert.equal(
    r.status, 0,
    `tar -tzf .audit-bin/actionlint.tar.gz failed (exit ${r.status}): ${r.stderr.trim()}. ` +
    "The archive may be truncated or corrupt."
  );
  const entries = r.stdout.trim().split("\n").filter(Boolean);
  assert.ok(entries.length > 0, "actionlint.tar.gz contains no entries — archive is empty after decompression");
  console.log(`OK  .audit-bin/actionlint.tar.gz is a valid archive (${entries.length} entr${entries.length === 1 ? "y" : "ies"})`);
}

// 5. actionlint.tar.gz contains an 'actionlint' binary entry.
//    Guards against accidentally committing the wrong tarball (e.g. a zizmor
//    release tarball in the actionlint slot), which would extract silently but
//    leave no usable binary on the expected PATH.
{
  const r = spawnSync("tar", ["-tzf", ACTIONLINT_TAR], { encoding: "utf8" });
  assert.equal(r.status, 0);
  const entries = r.stdout.trim().split("\n").filter(Boolean);
  // Match the bare filename (strip any leading directory components).
  const names = entries.map(e => e.split("/").pop());
  const hasActionlint = names.some(n => n === "actionlint" || n === "actionlint.exe");
  assert.ok(
    hasActionlint,
    `actionlint.tar.gz does not contain an 'actionlint' binary entry. ` +
    `Found: ${names.filter(Boolean).join(", ")}`
  );
  console.log("OK  actionlint.tar.gz contains an actionlint binary entry");
}

// 6. The loose binary and the tarball's actionlint entry are byte-identical.
//    Version skew (updating one but not the other) causes the skill to report
//    a different actionlint version depending on the install path taken, making
//    findings non-reproducible across machines.
{
  const tmpDir = mkdtempSync(join(tmpdir(), "audit-bin-test-"));
  try {
    const extract = spawnSync("tar", ["-xzf", ACTIONLINT_TAR, "-C", tmpDir], { encoding: "utf8" });
    assert.equal(extract.status, 0, `tar extract failed: ${extract.stderr.trim()}`);

    const findR = spawnSync(
      "find", [tmpDir, "-type", "f", "-name", "actionlint"],
      { encoding: "utf8" }
    );
    const extracted = findR.stdout.trim().split("\n").filter(Boolean)[0];
    assert.ok(extracted, "No 'actionlint' file found after extracting actionlint.tar.gz");

    const committedBytes = readFileSync(ACTIONLINT);
    const extractedBytes = readFileSync(extracted);
    assert.ok(
      committedBytes.equals(extractedBytes),
      ".audit-bin/actionlint and the binary inside actionlint.tar.gz are not byte-identical. " +
      "Update both together when upgrading the version pin in workflow-security-audit/SKILL.md."
    );
    console.log("OK  .audit-bin/actionlint is byte-identical to the entry inside actionlint.tar.gz");
  } finally {
    rmSync(tmpDir, { recursive: true, force: true });
  }
}

console.log("\nAll audit-bin tests passed.");
