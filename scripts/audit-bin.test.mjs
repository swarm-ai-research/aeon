// audit-bin.test.mjs — Integrity tests for pre-fetched scanner binaries in .audit-bin/
//
// The .audit-bin/ binaries (actionlint, zizmor) are committed to the repo so that
// workflow-security-audit can invoke them without hitting the runtime-install sandbox
// restriction (bash <(curl ...) and pipx install are both blocked in the GHA sandbox).
// These tests guard against the binaries being accidentally deleted, truncated, or
// having their execute bits stripped.
//
// Run: node scripts/audit-bin.test.mjs

import { accessSync, constants, existsSync, statSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { spawnSync } from "node:child_process";
import assert from "node:assert/strict";

const REPO_ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");
const AUDIT_BIN = join(REPO_ROOT, ".audit-bin");

// 1. actionlint binary exists
{
  assert.ok(existsSync(join(AUDIT_BIN, "actionlint")), ".audit-bin/actionlint must exist");
  console.log("OK  .audit-bin/actionlint exists");
}

// 2. actionlint is executable
{
  try {
    accessSync(join(AUDIT_BIN, "actionlint"), constants.X_OK);
  } catch {
    assert.fail(".audit-bin/actionlint must have execute permission (chmod +x)");
  }
  console.log("OK  .audit-bin/actionlint is executable");
}

// 3. zizmor binary exists
{
  assert.ok(existsSync(join(AUDIT_BIN, "zizmor")), ".audit-bin/zizmor must exist");
  console.log("OK  .audit-bin/zizmor exists");
}

// 4. zizmor is executable
{
  try {
    accessSync(join(AUDIT_BIN, "zizmor"), constants.X_OK);
  } catch {
    assert.fail(".audit-bin/zizmor must have execute permission (chmod +x)");
  }
  console.log("OK  .audit-bin/zizmor is executable");
}

// 5. actionlint.tar.gz exists and is not executable — it is a source archive, not a binary
{
  const archive = join(AUDIT_BIN, "actionlint.tar.gz");
  assert.ok(existsSync(archive), ".audit-bin/actionlint.tar.gz must exist");
  const st = statSync(archive);
  assert.ok(st.size > 0, ".audit-bin/actionlint.tar.gz must not be empty");
  assert.equal((st.mode & 0o111), 0, ".audit-bin/actionlint.tar.gz must not be executable (it is a source archive)");
  console.log("OK  .audit-bin/actionlint.tar.gz exists, non-empty, not executable");
}

// 6. Binaries are non-trivially sized — guards against a truncated or placeholder
//    file being accidentally committed in place of the real binary.
{
  const MIN_BYTES = 1_000_000; // 1 MB
  const actionlintSize = statSync(join(AUDIT_BIN, "actionlint")).size;
  const zizmorSize = statSync(join(AUDIT_BIN, "zizmor")).size;
  assert.ok(
    actionlintSize >= MIN_BYTES,
    `.audit-bin/actionlint is only ${actionlintSize} bytes — expected ≥1 MB; may be a stub or corrupted download`
  );
  assert.ok(
    zizmorSize >= MIN_BYTES,
    `.audit-bin/zizmor is only ${zizmorSize} bytes — expected ≥1 MB; may be a stub or corrupted download`
  );
  console.log(
    `OK  binary sizes: actionlint ${(actionlintSize / 1e6).toFixed(1)} MB, zizmor ${(zizmorSize / 1e6).toFixed(1)} MB`
  );
}

// 7. actionlint --version exits 0 and emits a semver string.
//    actionlint is statically linked (no shared-library dependencies), so this works
//    in the GHA sandbox even without any runtime install.
{
  const r = spawnSync(join(AUDIT_BIN, "actionlint"), ["--version"], {
    encoding: "utf8",
    timeout: 10_000,
  });
  assert.equal(r.status, 0, `actionlint --version exited ${r.status}; stderr: ${r.stderr}`);
  const firstLine = r.stdout.split("\n")[0].trim();
  assert.match(
    firstLine,
    /^\d+\.\d+\.\d+$/,
    `actionlint --version first line must be a semver string; got: ${JSON.stringify(r.stdout)}`
  );
  console.log(`OK  actionlint --version → ${firstLine}`);
}

console.log("\nAll audit-bin tests passed.");
