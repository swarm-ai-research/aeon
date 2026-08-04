// audit-bin.test.mjs — Smoke tests for the pre-committed scanner binaries.
//
// These executables live in .audit-bin/ so the workflow-security-audit skill
// can run them on GitHub Actions runners where outbound installs (pipx, curl)
// are blocked by the sandbox.  The tests here guard against:
//   - accidental chmod loss during a git checkout
//   - binary/version-pin drift between the committed file and SKILL.md
//   - a corrupt or wrong-content tar.gz
//
// Keep ACTIONLINT_VERSION and ZIZMOR_VERSION in sync with
// skills/workflow-security-audit/SKILL.md.
//
// Run: node .audit-bin/audit-bin.test.mjs

import { accessSync, statSync, constants } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { spawnSync } from 'node:child_process';

const DIR = dirname(fileURLToPath(import.meta.url));

const ACTIONLINT_VERSION = '1.7.12';
const ZIZMOR_VERSION = '1.25.2';

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

function fileOk(name, flag) {
  try { accessSync(join(DIR, name), flag); return true; } catch { return false; }
}

// ── actionlint ──────────────────────────────────────────────────

console.log('actionlint');

assert(fileOk('actionlint', constants.F_OK), 'binary exists');
assert(fileOk('actionlint', constants.X_OK), 'binary is executable');
assert(statSync(join(DIR, 'actionlint')).size > 1_000_000, 'binary size > 1 MB');

{
  const r = spawnSync(join(DIR, 'actionlint'), ['--version'], { encoding: 'utf8' });
  assert(r.status === 0, `--version exits 0 (got ${r.status ?? 'null'})`);
  const out = (r.stdout ?? '') + (r.stderr ?? '');
  assert(out.includes(ACTIONLINT_VERSION), `--version output contains ${ACTIONLINT_VERSION} (got: ${out.trim()})`);
}

// ── actionlint.tar.gz ───────────────────────────────────────────

console.log('actionlint.tar.gz');

assert(fileOk('actionlint.tar.gz', constants.F_OK), 'archive exists');
assert(statSync(join(DIR, 'actionlint.tar.gz')).size > 100_000, 'archive size > 100 KB');

{
  const r = spawnSync('tar', ['tzf', join(DIR, 'actionlint.tar.gz')], { encoding: 'utf8' });
  assert(r.status === 0, `tar tzf exits 0 (got ${r.status ?? 'null'})`);
  const entries = (r.stdout ?? '').trim().split('\n').filter(Boolean);
  assert(
    entries.some(e => e === 'actionlint' || e.endsWith('/actionlint')),
    `archive contains actionlint entry (found: ${entries.join(', ')})`,
  );
}

// ── zizmor ─────────────────────────────────────────────────────

console.log('zizmor');

assert(fileOk('zizmor', constants.F_OK), 'binary exists');
assert(fileOk('zizmor', constants.X_OK), 'binary is executable');
assert(statSync(join(DIR, 'zizmor')).size > 1_000_000, 'binary size > 1 MB');

{
  const r = spawnSync(join(DIR, 'zizmor'), ['--version'], { encoding: 'utf8' });
  assert(r.status === 0, `--version exits 0 (got ${r.status ?? 'null'})`);
  const out = (r.stdout ?? '') + (r.stderr ?? '');
  assert(out.includes(ZIZMOR_VERSION), `--version output contains ${ZIZMOR_VERSION} (got: ${out.trim()})`);
}

// ── results ────────────────────────────────────────────────────

console.log(`\n${passed} passed, ${failed} failed`);
if (failed > 0) throw new Error(`${failed} test(s) failed`);
