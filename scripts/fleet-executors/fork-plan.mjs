// fork-plan.mjs — Decisions the forker makes, as pure functions.
//
// `gl mirror` creates the destination repo on the node before it copies refs.
// Since 2026-06-06 the node refuses creation without an iCaptcha proof the CLI
// cannot send, so every mirror of an already-mirrored repo fails at a step that
// had nothing left to do — and because the forker fails the whole task if any
// target fails, the fork task has been red every day since.
//
// Splitting the decision out keeps it testable without a node or the CLI.

/**
 * What to do with one fork target, given whether its destination already
 * exists on the node.
 *
 * A github-mirror whose destination is already present skips the mirror: the
 * refs can't be refreshed while creation is gated, and attempting it only
 * produces a failure that masks the targets that genuinely need attention.
 */
export function planMirror({ kind, destExists }) {
  if (kind !== "github-mirror") return { action: "skip", reason: "not-a-mirror" };
  if (destExists) return { action: "skip", reason: "destination-exists" };
  return { action: "mirror", reason: "destination-missing" };
}

/**
 * Turn a `gl mirror` failure into something a reader can act on.
 *
 * The CLI reports the node's 403 as a bare "failed to create repo", so the
 * cause — a human-solved challenge — is invisible in the task result unless we
 * name it here.
 */
export function describeMirrorFailure(text) {
  var t = String(text || "");
  if (/icaptcha|captcha proof/i.test(t)) {
    return "node requires an iCaptcha proof to create a repo (solve at icaptcha.gitlawb.com, level >= 3)";
  }
  if (/failed to create repo/i.test(t)) {
    return "node refused repo creation — likely the iCaptcha gate; `gl mirror` does not surface the response body";
  }
  if (/could not read|repository not found|fatal: could not read/i.test(t)) {
    return "source repo is not readable anonymously — check the URL exists and is public";
  }
  return t.replace(/\s+/g, " ").slice(0, 160);
}
