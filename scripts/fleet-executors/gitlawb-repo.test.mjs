// gitlawb-repo.test.mjs — Tests for gitlawbRepoRef.
//
// Pure env-in/string-out; no CLI, filesystem, or network access.
//
// Run: node --test scripts/fleet-executors/gitlawb-repo.test.mjs

import { test } from "node:test";
import assert from "node:assert/strict";
import { gitlawbRepoRef, DEFAULT_GITLAWB_REPO_URL } from "./gitlawb-repo.mjs";

const OWNER = "did:key:z6MkpiXbCJzXGLw9bQXw5t8ja734YsrhYWEQMqsicwUcjHbH";

test("keeps the pre-fix bare ref when nothing is configured", () => {
  assert.equal(gitlawbRepoRef({}), "aeon");
});

test("derives the owner from GITLAWB_REPO_URL", () => {
  const other = "did:key:z6MkpbhwfdMK2hLgqFEUKytP6PGGuTsT5bY4d1Pdz6vxcHQ6";
  assert.equal(
    gitlawbRepoRef({ GITLAWB_REPO_URL: `gitlawb://${other}/aeon` }),
    `${other}/aeon`,
  );
});

test("accepts a repo URL without the gitlawb:// scheme or with a .git suffix", () => {
  assert.equal(gitlawbRepoRef({ GITLAWB_REPO_URL: `${OWNER}/aeon` }), `${OWNER}/aeon`);
  assert.equal(gitlawbRepoRef({ GITLAWB_REPO_URL: `gitlawb://${OWNER}/aeon.git` }), `${OWNER}/aeon`);
});

test("GITLAWB_ISSUE_REPO overrides the derived ref", () => {
  const ref = gitlawbRepoRef({
    GITLAWB_ISSUE_REPO: "did:key:zOverride/notes",
    GITLAWB_REPO_URL: `gitlawb://${OWNER}/aeon`,
  });
  assert.equal(ref, "did:key:zOverride/notes");
});

test("blank env values fall through instead of yielding an empty ref", () => {
  assert.equal(gitlawbRepoRef({ GITLAWB_ISSUE_REPO: "  ", GITLAWB_REPO_URL: "" }), "aeon");
  assert.equal(gitlawbRepoRef({ GITLAWB_ISSUE_REPO: "  ", GITLAWB_REPO_URL: `gitlawb://${OWNER}/aeon` }), `${OWNER}/aeon`);
});

test("falls back to the bare repo name when the URL carries no owner DID", () => {
  assert.equal(gitlawbRepoRef({ GITLAWB_REPO_URL: "gitlawb://aeon" }), "aeon");
  assert.equal(gitlawbRepoRef({ GITLAWB_REPO_URL: "not-a-url" }), "aeon");
});

test("the default URL is a parseable gitlawb ref", () => {
  assert.match(DEFAULT_GITLAWB_REPO_URL, /^gitlawb:\/\/did:key:[^/]+\/.+$/);
});
