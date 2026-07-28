/**
 * audit-bin.test.mjs — Smoke tests for the committed .audit-bin/ executables.
 *
 * The workflow-security-audit skill selects tools via `[ -x ".audit-bin/zizmor" ]`
 * and `[ -x ".audit-bin/actionlint" ]`. This file tests that both binaries are
 * present, executable, and respond to --version, and that the tarball is readable.
 *
 * Run: node scripts/audit-bin.test.mjs
 */

import { accessSync, statSync, constants } from "node:fs";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const REPO_ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");
const AUDIT_BIN = join(REPO_ROOT, ".audit-bin");

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

function isExecutable(p) {
  try { accessSync(p, constants.X_OK); return true; } catch { return false; }
}

function fileExists(p) {
  try { statSync(p); return true; } catch { return false; }
}

// ── actionlint ────────────────────────────────────────────────

console.log("actionlint:");
{
  const bin = join(AUDIT_BIN, "actionlint");
  assert(fileExists(bin), "binary exists at .audit-bin/actionlint");
  assert(isExecutable(bin), "binary is executable ([ -x .audit-bin/actionlint ] → true)");

  const r = spawnSync(bin, ["--version"], { encoding: "utf8", timeout: 5000 });
  assert(r.status === 0, "--version exits 0");
  assert(typeof r.stdout === "string" && r.stdout.trim().length > 0, "--version prints a non-empty version string");
}

// ── actionlint.tar.gz ─────────────────────────────────────────

console.log("\nactionlint.tar.gz:");
{
  const tarball = join(AUDIT_BIN, "actionlint.tar.gz");
  assert(fileExists(tarball), "tarball exists at .audit-bin/actionlint.tar.gz");
  const stat = statSync(tarball);
  assert(stat.size > 0, "tarball is non-empty");

  // Verify the archive lists an 'actionlint' entry without extracting it.
  const r = spawnSync("tar", ["-tzf", tarball], { encoding: "utf8", timeout: 10000 });
  assert(r.status === 0, "tar -tzf succeeds (archive is valid gzip+tar)");
  assert(
    (r.stdout || "").split("\n").some((line) => /actionlint$/.test(line.trim())),
    "archive contains an entry named 'actionlint'"
  );
}

// ── zizmor ────────────────────────────────────────────────────

console.log("\nzizmor:");
{
  const bin = join(AUDIT_BIN, "zizmor");
  assert(fileExists(bin), "binary exists at .audit-bin/zizmor");
  assert(isExecutable(bin), "binary is executable ([ -x .audit-bin/zizmor ] → true)");

  const r = spawnSync(bin, ["--version"], { encoding: "utf8", timeout: 5000 });
  assert(r.status === 0, "--version exits 0");
  assert(typeof r.stdout === "string" && r.stdout.trim().length > 0, "--version prints a non-empty version string");
}

// ── Results ───────────────────────────────────────────────────

console.log(`\n${passed} passed, ${failed} failed`);
if (failed > 0) throw new Error(`${failed} test(s) failed`);
