// fork-plan.test.mjs — Tests for planMirror / describeMirrorFailure.
//
// Pure functions; no node, CLI, or filesystem access.
//
// Run: node --test scripts/fleet-executors/fork-plan.test.mjs

import { test } from "node:test";
import assert from "node:assert/strict";
import { planMirror, describeMirrorFailure } from "./fork-plan.mjs";

test("mirrors a github source whose destination is missing", () => {
  assert.deepEqual(planMirror({ kind: "github-mirror", destExists: false }),
                   { action: "mirror", reason: "destination-missing" });
});

test("skips the mirror when the destination is already on the node", () => {
  // The regression this fixes: `gl mirror` would try to create an existing repo
  // and be refused, failing the whole fork task.
  assert.deepEqual(planMirror({ kind: "github-mirror", destExists: true }),
                   { action: "skip", reason: "destination-exists" });
});

test("leaves non-mirror targets alone", () => {
  assert.equal(planMirror({ kind: "fork-only", destExists: false }).action, "skip");
  assert.equal(planMirror({ kind: undefined, destExists: false }).reason, "not-a-mirror");
});

test("names the iCaptcha gate when the node says so outright", () => {
  var msg = describeMirrorFailure("create failed (403 Forbidden): iCaptcha proof required (missing proof header).");
  assert.match(msg, /iCaptcha proof/);
  assert.match(msg, /icaptcha\.gitlawb\.com/);
});

test("infers the gate from the CLI's bare creation error", () => {
  // What `gl mirror` actually prints — it drops the response body.
  var msg = describeMirrorFailure("Cloning into bare repository '/tmp/gl-mirror-abc/aeon'...\nError: failed to create repo");
  assert.match(msg, /refused repo creation/);
  assert.match(msg, /iCaptcha/);
});

test("distinguishes an unreadable source from a node-side refusal", () => {
  var msg = describeMirrorFailure("fatal: could not read Username for 'https://github.com': No such device or address");
  assert.match(msg, /not readable anonymously/);
  assert.doesNotMatch(msg, /iCaptcha/);
});

test("passes through an unrecognized error, collapsed and bounded", () => {
  var msg = describeMirrorFailure("something\n  unexpected   happened");
  assert.equal(msg, "something unexpected happened");
  assert.ok(describeMirrorFailure("x".repeat(400)).length <= 160);
});

test("handles empty and missing input without throwing", () => {
  assert.equal(describeMirrorFailure(""), "");
  assert.equal(describeMirrorFailure(null), "");
  assert.equal(describeMirrorFailure(undefined), "");
});
