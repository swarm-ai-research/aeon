// audit-bin.test.mjs — Sanity checks for the pre-committed scanner binaries.
//
// The workflow-security-audit SKILL.md bootstraps by preferring `.audit-bin/`
// over network installs (pipx / pip).  These tests assert the prerequisites
// that bootstrap logic assumes are true.
//
// Run: node .audit-bin/audit-bin.test.mjs

import { statSync, readFileSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import assert from "node:assert/strict";

const HERE = dirname(fileURLToPath(import.meta.url));
const ROOT = join(HERE, "..");

const ZIZMOR      = join(HERE, "zizmor");
const ACTIONLINT  = join(HERE, "actionlint");
const AL_TGZ      = join(HERE, "actionlint.tar.gz");
const SKILL_MD    = join(ROOT, "skills/workflow-security-audit/SKILL.md");

// Returns true when any exec bit (owner / group / other) is set.
function isExecutable(path) {
  return (statSync(path).mode & 0o111) !== 0;
}

// 1. Both binaries must exist as regular files.
assert.doesNotThrow(() => statSync(ZIZMOR),     "zizmor binary must be present at .audit-bin/zizmor");
assert.doesNotThrow(() => statSync(ACTIONLINT), "actionlint binary must be present at .audit-bin/actionlint");
assert.equal(statSync(ZIZMOR).isFile(),     true, "zizmor must be a regular file, not a directory or symlink");
assert.equal(statSync(ACTIONLINT).isFile(), true, "actionlint must be a regular file");
console.log("OK  both binaries exist as regular files");

// 2. Both binaries must have the executable bit set.
//    The SKILL.md bootstrap uses `if [ -x ".audit-bin/zizmor" ]` — if the bit
//    is missing the skill silently falls through to a network install, which may
//    be blocked in the GHA sandbox.
assert.equal(
  isExecutable(ZIZMOR), true,
  "zizmor must be executable; a missing exec bit causes the skill to fall through to a pipx install"
);
assert.equal(
  isExecutable(ACTIONLINT), true,
  "actionlint must be executable; a missing exec bit causes the skill to fall through to a curl install"
);
console.log("OK  both binaries have the executable bit set");

// 3. The tar.gz archive must exist but must NOT be executable.
//    It is source material for re-building the binary, not a runnable file.
//    If it were accidentally chmod +x'd it could be confused with the binary in
//    scripts that rely on `[ -x ]` checks over the whole directory.
assert.doesNotThrow(() => statSync(AL_TGZ), "actionlint.tar.gz must be present");
assert.equal(statSync(AL_TGZ).isFile(), true, "actionlint.tar.gz must be a regular file");
assert.equal(
  isExecutable(AL_TGZ), false,
  "actionlint.tar.gz must not have the executable bit set — it is an archive, not a binary"
);
console.log("OK  actionlint.tar.gz present and non-executable");

// 4. SKILL.md must contain a ZIZMOR_VERSION pin with valid semver shape.
//    Bumping the binary without updating the pin (or vice versa) causes the
//    pip-install fallback path to install a different version than the committed
//    binary, breaking reproducibility across environments.
const skillMd = readFileSync(SKILL_MD, "utf8");
const versionMatch = skillMd.match(/ZIZMOR_VERSION="(\d+\.\d+\.\d+)"/);
assert.ok(
  versionMatch,
  'SKILL.md must contain a ZIZMOR_VERSION="X.Y.Z" line; missing pin breaks the pip-install fallback'
);
const [, pinnedVersion] = versionMatch;
assert.match(pinnedVersion, /^\d+\.\d+\.\d+$/, "ZIZMOR_VERSION must be a three-part semver");
console.log(`OK  SKILL.md pins ZIZMOR_VERSION="${pinnedVersion}" (valid semver)`);

// 5. The version pin must not be a placeholder.
//    Guards against accidentally committing ZIZMOR_VERSION="0.0.0" or a blank string.
assert.notEqual(pinnedVersion, "0.0.0", "ZIZMOR_VERSION must not be the placeholder 0.0.0");
assert.ok(
  parseInt(pinnedVersion.split(".")[0], 10) >= 1,
  "ZIZMOR_VERSION major must be ≥ 1; zizmor has been stable since 1.x"
);
console.log("OK  ZIZMOR_VERSION pin is non-trivial (major ≥ 1, not a zero placeholder)");

// 6. The SKILL.md must reference `.audit-bin/` as the primary binary source.
//    Regression guard: if the bootstrap section is edited away, the skill loses
//    its ability to use committed binaries and silently degrades to network installs.
assert.match(
  skillMd,
  /\.audit-bin\/zizmor/,
  "SKILL.md must reference .audit-bin/zizmor as the primary binary path"
);
assert.match(
  skillMd,
  /\.audit-bin\/actionlint/,
  "SKILL.md must reference .audit-bin/actionlint as the primary binary path"
);
console.log("OK  SKILL.md references both .audit-bin/ binaries in its bootstrap section");

console.log("\nAll audit-bin sanity tests passed.");
