// Observability for the safety layer.
//
// Every safety-relevant decision (spawn, renew pass/fail, kill/revoke,
// authorization allow/deny, self-evolution review, merge, dispatch) is emitted
// as an event into a MetricsRecorder. `aggregate` rolls a window of events into
// a snapshot; `snapshotToMarkdown` renders it for `./notify` (which fans out to
// the dashboard via notify-jsonrender). Recording is OPTIONAL everywhere — the
// recorder is just an object with `.record(type, fields)`, so components that
// aren't given one behave exactly as before.

import { appendFileSync, readFileSync, existsSync, mkdirSync } from "node:fs";
import { dirname } from "node:path";

export class MetricsRecorder {
  constructor({ path = null, keep = 5000 } = {}) {
    this.path = path;
    this.keep = keep;
    this.events = [];
    if (path && existsSync(path)) {
      this.events = readFileSync(path, "utf8")
        .trim()
        .split("\n")
        .filter(Boolean)
        .map((l) => JSON.parse(l));
    }
  }

  record(type, fields = {}) {
    const event = { ts: Math.floor(Date.now() / 1000), type, ...fields };
    this.events.push(event);
    if (this.events.length > this.keep) this.events.splice(0, this.events.length - this.keep);
    if (this.path) {
      mkdirSync(dirname(this.path), { recursive: true });
      appendFileSync(this.path, JSON.stringify(event) + "\n");
    }
    return event;
  }

  all() {
    return this.events;
  }
}

function tally(values) {
  const out = {};
  for (const v of values) out[v] = (out[v] ?? 0) + 1;
  return out;
}

// Roll events (+ optional live instance list) into a snapshot.
export function aggregate(events, { now = Math.floor(Date.now() / 1000), windowSeconds = 86400, instances = [] } = {}) {
  const win = events.filter((e) => e.ts >= now - windowSeconds);
  const of = (type) => win.filter((e) => e.type === type);

  const renew = of("renew");
  const renewPass = renew.filter((e) => e.renewed).length;
  const auth = of("authorize");
  const authAllow = auth.filter((e) => e.allowed).length;
  const review = of("review");
  const reviewApproved = review.filter((e) => e.approved).length;
  const merge = of("merge_authorize");
  const mergeAllow = merge.filter((e) => e.allowed).length;
  const bridge = of("bridge");
  const task = of("task");
  const taskOk = task.filter((e) => e.ok).length;

  return {
    window: windowSeconds,
    now,
    instances: { total: instances.length, byStatus: tally(instances.map((i) => i.health ?? i.status ?? "unknown")) },
    spawns: of("spawn").length,
    kills: of("kill").length,
    dispatches: of("dispatch").length,
    tasks: { total: task.length, ok: taskOk, fail: task.length - taskOk },
    renewals: { total: renew.length, pass: renewPass, fail: renew.length - renewPass },
    authorizations: {
      total: auth.length,
      allow: authAllow,
      deny: auth.length - authAllow,
      denialReasons: tally(auth.filter((e) => !e.allowed).map((e) => e.reason)),
    },
    reviews: {
      total: review.length,
      approved: reviewApproved,
      refused: review.length - reviewApproved,
      refusalStages: tally(review.filter((e) => !e.approved).map((e) => e.stage)),
    },
    merges: { total: merge.length, allow: mergeAllow, deny: merge.length - mergeAllow },
    bridge: { total: bridge.length, deny: bridge.filter((e) => e.decision === "deny").length },
  };
}

function pct(n, d) {
  return d ? `${Math.round((100 * n) / d)}%` : "—";
}

export function snapshotToMarkdown(s) {
  const inst = Object.entries(s.instances.byStatus)
    .map(([k, v]) => `${k} ${v}`)
    .join(" · ") || "none";
  const denials = Object.entries(s.authorizations.denialReasons)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 5)
    .map(([r, n]) => `- ${r} — ${n}`)
    .join("\n");

  const lines = [
    `*GitLawb Fleet — Observability (${Math.round(s.window / 3600)}h)*`,
    ``,
    `Instances: ${s.instances.total} total (${inst})`,
    `Spawns: ${s.spawns} · Kills/revokes: ${s.kills} · Dispatches: ${s.dispatches}`,
    `Tasks: ${s.tasks.ok}/${s.tasks.total} ok (${pct(s.tasks.ok, s.tasks.total)}) · failed ${s.tasks.fail}`,
    `Renewals: ${s.renewals.pass}/${s.renewals.total} passed (${pct(s.renewals.pass, s.renewals.total)}) · failed ${s.renewals.fail}`,
    `Authorizations: allow ${s.authorizations.allow} · deny ${s.authorizations.deny}`,
    `Merge gate: approved ${s.merges.allow} · denied ${s.merges.deny} · reviews refused ${s.reviews.refused}`,
  ];
  if (s.bridge.total) lines.push(`Bridge: ${s.bridge.total} events · ${s.bridge.deny} denied`);
  if (denials) lines.push(``, `Top denial reasons:`, denials);
  return lines.join("\n");
}
