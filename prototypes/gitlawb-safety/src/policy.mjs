// Automated safety check used to gate capability renewal.
//
// This is the cheap, always-on first line — the interface a red-team sub-swarm
// later plugs into unchanged. It receives a description of what the agent has
// been doing and returns { pass, reason }. Renewal proceeds only on pass; a
// fail lets the capability expire at its (short) TTL.
//
// The default policy is deliberately conservative: it approves only changes
// that are small and confined to an allowlisted set of paths, and it hard-
// blocks self-modification of the safety machinery itself.

import { isSafetyCritical } from "./caps.mjs";

const DEFAULT = {
  maxChangedFiles: 25,
  maxChangedLines: 1500,
  // Paths an evolving agent may touch. Anything outside → refuse renewal.
  allowedPathPrefixes: ["skills/", "articles/", "memory/", "dashboard/"],
  // Paths no agent may ever rewrite — the gate must live outside the agent's
  // reach (risk #5: self-evolution must not evolve away its own oversight).
  protectedPathPrefixes: [
    "prototypes/gitlawb-safety/src/",
    ".github/workflows/",
    "CLAUDE.md",
    // Task artifacts hold reviewer renewal verdicts (see src/reviewer-gate.mjs).
    // No agent diff may write here, or an agent could forge its own approval.
    "memory/gitlawb-runner/",
  ],
};

// `opts.redTeam` (optional) is an async adversarial reviewer with the same
// shape as this check — see src/reviewer-gate.mjs. When supplied, it runs as a SECOND
// stage AFTER the cheap rule checks pass: defense in depth. It fails closed, so
// an error/timeout in the reviewer denies renewal rather than letting it
// through unreviewed. Omit it (the default) for rules-only behaviour.
export function makePolicyCheck(opts = {}) {
  const { redTeam, ...rest } = opts;
  const cfg = { ...DEFAULT, ...rest };

  return async function safetyCheck(ctx) {
    const { audienceDid, capabilities, activity } = ctx ?? {};
    const a = activity ?? {};
    const needsActivity = (capabilities ?? []).some((c) => isSafetyCritical(c.can));
    if (needsActivity && !activity) {
      return { pass: false, reason: "missing_activity" };
    }
    const changedFiles = a.changedFiles ?? [];
    const changedLines = a.changedLines ?? 0;

    const protectedHit = changedFiles.find((f) =>
      cfg.protectedPathPrefixes.some((p) => f.startsWith(p)),
    );
    if (protectedHit) {
      return { pass: false, reason: `touched_protected_path:${protectedHit}` };
    }

    const outside = changedFiles.find(
      (f) => !cfg.allowedPathPrefixes.some((p) => f.startsWith(p)),
    );
    if (outside) return { pass: false, reason: `path_not_allowlisted:${outside}` };

    if (changedFiles.length > cfg.maxChangedFiles) {
      return { pass: false, reason: `too_many_files:${changedFiles.length}` };
    }
    if (changedLines > cfg.maxChangedLines) {
      return { pass: false, reason: `diff_too_large:${changedLines}` };
    }

    // Stage 2 — adversarial red-team review (only for safety-critical caps,
    // and only once the rules have cleared). Fail closed on any error.
    if (redTeam && needsActivity) {
      try {
        const rt = await redTeam(ctx);
        if (!rt || rt.pass !== true) {
          return { pass: false, reason: rt?.reason || "redteam_flagged", findings: rt?.findings, stage: "red-team" };
        }
      } catch (err) {
        return { pass: false, reason: "redteam_error", stage: "red-team", findings: String(err?.message ?? err).slice(0, 120) };
      }
    }

    return { pass: true };
  };
}
