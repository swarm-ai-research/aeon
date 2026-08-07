// gitlawb-repo.mjs — Resolve the GitLawb repo ref a fleet executor writes to.
//
// `gl issue create ... aeon` resolves a bare repo name under the *runner's own*
// DID. That happens to work for the private fleet, whose operator owns `aeon`,
// but 404s for every other operator — the public-mirror fleet owns no repos, so
// each of its code-review and audit tasks died with
//   create issue failed (404 Not Found): repository '<operator-did>/aeon' not found
//
// Qualify the ref with the owner DID from GITLAWB_REPO_URL instead — the same
// URL deployer.mjs pushes signed proofs to — so every fleet writes to the repo
// that actually holds the fleet's paper trail, whatever identity it runs as.
// `gl` accepts both `<owner>/<repo>` and bare `<repo>`.

// Clone URL for the GitLawb-hosted repo the private fleet pushes proofs to.
// Only deployer.mjs needs a URL (you can't `git clone` a bare repo name); the
// ref resolver below deliberately does NOT fall back to it — see gitlawbRepoRef.
export const DEFAULT_GITLAWB_REPO_URL =
  "gitlawb://did:key:z6MkpiXbCJzXGLw9bQXw5t8ja734YsrhYWEQMqsicwUcjHbH/aeon";

/**
 * Repo argument for `gl issue create` / `gl pr list`, as `<owner-did>/<repo>`.
 *
 * GITLAWB_ISSUE_REPO wins when set (escape hatch for a fleet that reads and
 * writes different repos); otherwise the ref is derived from GITLAWB_REPO_URL,
 * which the fleet-runner workflow sets.
 *
 * With neither set this returns the bare `aeon` — the pre-fix behavior, where
 * `gl` resolves under the runner's own DID. That fallback is deliberate: an
 * unconfigured fleet should fail the way it does today rather than silently
 * write into another identity's repo.
 */
export function gitlawbRepoRef(env = process.env) {
  const explicit = (env.GITLAWB_ISSUE_REPO || "").trim();
  if (explicit) return explicit;

  const url = (env.GITLAWB_REPO_URL || "").trim();
  const stripped = url.replace(/^gitlawb:\/\//, "").replace(/\.git$/, "");
  const match = stripped.match(/^(did:key:[^/]+)\/(.+)$/);
  return match ? `${match[1]}/${match[2]}` : "aeon";
}
