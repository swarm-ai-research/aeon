// goal-store.mjs — Runtime backlog of operational goals for the Aeon fleet.
//
// The `## Goals` section in memory/MEMORY.md is the source of truth for *what*
// the fleet should be doing. goal-tracker reads it to report status. This
// module is the *operational* counterpart: it tracks the per-goal scheduling
// state (when last attempted, what to try next, who owns it) so the fleet can
// chip at long-horizon goals across many 15-min cycles instead of only firing
// reactive cooldown-gated tasks.
//
// File layout:
//   memory/fleet-goals/backlog.json — {version, goals: [...]}
//
// Goal record shape — see memory/fleet-goals/README.md for field semantics.

import { existsSync, readFileSync, writeFileSync, mkdirSync } from "node:fs";
import { dirname } from "node:path";

export const BACKLOG_VERSION = 1;

export const VALID_STATUSES = new Set(["active", "paused", "done"]);
export const VALID_ROLES = new Set(["researcher", "reviewer", "deployer", "sentinel"]);

export function loadBacklog(path) {
  if (!existsSync(path)) return { version: BACKLOG_VERSION, goals: [] };
  const raw = JSON.parse(readFileSync(path, "utf8"));
  if (!raw || typeof raw !== "object") return { version: BACKLOG_VERSION, goals: [] };
  return {
    version: raw.version || BACKLOG_VERSION,
    goals: Array.isArray(raw.goals) ? raw.goals : [],
  };
}

export function saveBacklog(path, backlog) {
  mkdirSync(dirname(path), { recursive: true });
  writeFileSync(path, JSON.stringify(backlog, null, 2) + "\n");
}

export function validateGoal(g) {
  const errs = [];
  if (!g.id || typeof g.id !== "string") errs.push("id required");
  if (!g.title) errs.push("title required");
  if (!VALID_ROLES.has(g.owner_role)) errs.push(`owner_role must be one of ${[...VALID_ROLES].join(",")}`);
  if (!g.kind) errs.push("kind required");
  if (!g.capability) errs.push("capability required");
  if (!VALID_STATUSES.has(g.status || "active")) errs.push("status invalid");
  if (g.cadence_hours != null && (typeof g.cadence_hours !== "number" || g.cadence_hours < 0)) {
    errs.push("cadence_hours must be a non-negative number");
  }
  return errs;
}

// Round-robin scheduler with a cadence gate.
//
// "Due" = active, not paused, and (last_attempted_at == null OR
// last_attempted_at + cadence_hours <= now). Ordered by oldest-attempt-first
// so a fresh goal can't starve older ones — important once the backlog grows.
// Capped at maxPerCycle so one cycle can't flood the fleet.
export function pickDueGoals(backlog, now, maxPerCycle) {
  const due = [];
  for (const g of backlog.goals) {
    if ((g.status || "active") !== "active") continue;
    const cadenceH = g.cadence_hours ?? 0;
    if (g.last_attempted_at) {
      const last = new Date(g.last_attempted_at).getTime();
      if (Number.isNaN(last)) continue;
      const eligibleAt = last + cadenceH * 3600 * 1000;
      if (eligibleAt > now.getTime()) continue;
    }
    due.push(g);
  }
  due.sort((a, b) => {
    const ta = a.last_attempted_at ? new Date(a.last_attempted_at).getTime() : 0;
    const tb = b.last_attempted_at ? new Date(b.last_attempted_at).getTime() : 0;
    return ta - tb;
  });
  return due.slice(0, maxPerCycle);
}

export function markAttempted(backlog, goalId, iso) {
  const g = backlog.goals.find((x) => x.id === goalId);
  if (!g) return false;
  g.last_attempted_at = iso;
  return true;
}

// ── Spawn log ─────────────────────────────────────────────────
//
// Each goal spawn records {spawned_at, goal_id, task_id} so outcome
// reconciliation can later link a completed/failed task back to the goal
// that produced it. metrics.jsonl has no payload, and failed tasks leave
// no artifact, so the reconciler keeps its own ledger.

export const RESOLVED_TTL_DAYS = 7;

export function loadSpawns(path) {
  if (!existsSync(path)) return [];
  try {
    const raw = JSON.parse(readFileSync(path, "utf8"));
    return Array.isArray(raw) ? raw : [];
  } catch {
    return [];
  }
}

export function saveSpawns(path, spawns, now) {
  mkdirSync(dirname(path), { recursive: true });
  const cutoff = now.getTime() - RESOLVED_TTL_DAYS * 24 * 3600 * 1000;
  const pruned = spawns.filter((s) => {
    if (!s.resolved_at) return true;
    return new Date(s.resolved_at).getTime() >= cutoff;
  });
  writeFileSync(path, JSON.stringify(pruned, null, 2) + "\n");
}

export function appendSpawn(spawns, entry) {
  spawns.push({
    spawned_at: entry.spawned_at,
    goal_id: entry.goal_id,
    task_id: entry.task_id,
  });
}

export function unresolvedSpawns(spawns) {
  return spawns.filter((s) => !s.resolved_at);
}

// `gl task create` returns the new task ID as a UUID — either bare or in a
// JSON envelope. Try JSON first, fall back to UUID regex.
const UUID_RE = /[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}/i;

export function extractTaskId(stdout) {
  if (!stdout) return null;
  const trimmed = stdout.trim();
  try {
    const j = JSON.parse(trimmed);
    if (j && typeof j === "object") {
      const candidate = j.task_id || j.taskId || j.id;
      if (candidate && typeof candidate === "string" && UUID_RE.test(candidate)) return candidate;
    }
  } catch {
    /* not JSON, fall through */
  }
  const m = trimmed.match(UUID_RE);
  return m ? m[0] : null;
}

// ── Outcome classification ────────────────────────────────────
//
// Outcomes: "advanced" | "noop" | "blocked" | "lost" | null (still pending)

const NOOP_PATTERNS = [
  /\bno[- ]?op(s|ped)?\b/i,
  /\bnothing to do\b/i,
  /\balready (done|complete|merged|resolved)\b/i,
  /\bskip(ped)?\b/i,
];

export function classifyOutcome({ artifact, metricsEvent, spawnedAt, now, lostAfterHours = 2 }) {
  if (artifact) {
    const summary = (artifact.result?.summary || "").toString();
    if (NOOP_PATTERNS.some((re) => re.test(summary))) return "noop";
    return "advanced";
  }
  if (metricsEvent && metricsEvent.ok === false) return "blocked";
  const ageMs = now.getTime() - new Date(spawnedAt).getTime();
  if (Number.isFinite(ageMs) && ageMs > lostAfterHours * 3600 * 1000) return "lost";
  return null;
}

// Mutate the goal with a classified outcome. Returns {autoPaused}.
// Auto-pause only triggers on the transition into paused — re-runs against
// an already-paused goal don't re-emit the signal.
export function applyOutcome(goal, outcome, now, noopLimit) {
  goal.last_outcome = outcome;
  goal.last_outcome_at = now.toISOString();
  if (outcome === "advanced") {
    goal.consecutive_noops = 0;
    return { autoPaused: false };
  }
  goal.consecutive_noops = (goal.consecutive_noops || 0) + 1;
  if (goal.consecutive_noops >= noopLimit && (goal.status || "active") === "active") {
    goal.status = "paused";
    goal.paused_reason = `auto-paused after ${goal.consecutive_noops} consecutive non-advanced outcomes (last: ${outcome})`;
    goal.paused_at = now.toISOString();
    return { autoPaused: true };
  }
  return { autoPaused: false };
}
