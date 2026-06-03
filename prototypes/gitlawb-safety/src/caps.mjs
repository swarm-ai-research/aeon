// Capability vocabulary, mirroring the constants defined in
// gitlawb-core/src/ucan.rs (`caps` module).

export const CAP = {
  GIT_PUSH: "git/push",
  GIT_FETCH: "git/fetch",
  PR_OPEN: "pr/open",
  PR_MERGE: "pr/merge",
  PR_REVIEW: "pr/review",
  ISSUE_CREATE: "issue/create",
  ISSUE_CLOSE: "issue/close",
  NETWORK_JOIN: "network/join",
  AGENT_DEPLOY: "agent/deploy",
  REPO_ADMIN: "repo/admin",
};

// The capabilities that let an agent spawn more agents or rewrite its own
// code. These get the strictest treatment: a hard short-TTL ceiling and
// mandatory renewal-gating. GitLawb itself enforces none of this.
export const SAFETY_CRITICAL = new Set([
  CAP.AGENT_DEPLOY,
  CAP.REPO_ADMIN,
  CAP.PR_MERGE,
]);

// Hard ceilings (seconds) on how long a freshly-minted capability may live.
// Because GitLawb has no revocation, expiry is the only real off-switch — so
// the dangerous capabilities are kept on a very short leash and must be
// continuously re-earned via gated renewal.
export const MAX_TTL = {
  default: 24 * 60 * 60, // 24h for ordinary read/low-risk caps
  safetyCritical: 5 * 60, // 5min for agent/deploy, repo/admin, pr/merge
};

export function isSafetyCritical(ability) {
  return SAFETY_CRITICAL.has(ability);
}

export function ceilingFor(ability) {
  return isSafetyCritical(ability) ? MAX_TTL.safetyCritical : MAX_TTL.default;
}

// A capability is { with: <resource URI>, can: <ability>, nb?: <constraints> }.
export function cap(resource, ability, constraints) {
  const c = { with: resource, can: ability };
  if (constraints) c.nb = constraints;
  return c;
}

// Attenuation check: is `child` permitted by `parent`?
// Same ability, and the child resource is equal to or scoped under the parent.
export function isAttenuationOf(child, parent) {
  if (child.can !== parent.can) return false;
  if (parent.with === "*") return true;
  if (child.with === parent.with) return true;
  // prefix scoping, e.g. parent "repo:foo/*" covers child "repo:foo/bar"
  if (parent.with.endsWith("/*")) {
    return child.with.startsWith(parent.with.slice(0, -1));
  }
  return false;
}
