/**
 * Aeon REST + SSE gateway (hxmp.4).
 *
 * A plain HTTP API for invoking skills with live progress, mirroring
 * fabro-server's run/event model (Axum `/runs` + SSE `attach`). This is the
 * ergonomic alternative to the A2A JSON-RPC envelope and the replacement for
 * the legacy `.outputs/` file-polling pattern: every run keeps an in-memory,
 * sequence-numbered event log, so a client can either stream it live over SSE
 * or poll `GET /runs/:id/events?since=N` for incremental progress.
 *
 * Routes (all under /api/v1):
 *   GET  /skills                 — list available skills
 *   GET  /skills/:slug           — one skill's metadata
 *   POST /runs                   — start a run: { skill, var? } → 201 { id, ... }
 *   GET  /runs                   — list runs (most recent first)
 *   GET  /runs/:id               — run status + result
 *   GET  /runs/:id/events?since= — buffered progress events after seq `since`
 *   GET  /runs/:id/stream        — SSE: backlog replay then live progress
 *   POST /runs/:id/cancel        — cancel an in-flight run
 */

import { IncomingMessage, ServerResponse } from "http";
import { randomUUID } from "crypto";
import {
  getSkills,
  getSkillBySlug,
  skillFileExists,
  buildSkillPrompt,
  defaultPlan,
  REPO_ROOT,
} from "./core.js";
import { runPrompt, type ProgressEvent } from "./llm-runner.js";

// ── Types ──────────────────────────────────────────────────────────────────

export type RunStatus = "queued" | "running" | "completed" | "failed" | "canceled";

interface RunEvent {
  /** Monotonic per-run sequence number, starting at 1. */
  seq: number;
  /** Event type: lifecycle transitions plus normalized progress kinds. */
  type: "status" | ProgressEvent["kind"];
  timestamp: string;
  data: Record<string, unknown>;
}

interface Run {
  id: string;
  skill: string;
  var: string;
  status: RunStatus;
  createdAt: string;
  updatedAt: string;
  result: string | null;
  error: string | null;
  events: RunEvent[];
  _seq: number;
  _subscribers: Set<ServerResponse>;
  _abort: AbortController;
  _completedAt?: number;
}

// ── State ──────────────────────────────────────────────────────────────────

const runs = new Map<string, Run>();
const RUN_TTL_MS = 30 * 60 * 1000; // 30 min, matches the A2A task TTL
const MAX_RUNS = 1000;

function evictStaleRuns(): void {
  const now = Date.now();
  for (const [id, run] of runs) {
    if (run._completedAt && now - run._completedAt > RUN_TTL_MS) runs.delete(id);
  }
  if (runs.size > MAX_RUNS) {
    const done = [...runs.entries()]
      .filter(([, r]) => r._completedAt)
      .sort((a, b) => (a[1]._completedAt ?? 0) - (b[1]._completedAt ?? 0));
    for (const [id] of done) {
      runs.delete(id);
      if (runs.size <= MAX_RUNS) break;
    }
  }
}

// ── Event recording + SSE fan-out ──────────────────────────────────────────

function emit(run: Run, type: RunEvent["type"], data: Record<string, unknown>): void {
  const event: RunEvent = {
    seq: ++run._seq,
    type,
    timestamp: new Date().toISOString(),
    data,
  };
  run.events.push(event);
  run.updatedAt = event.timestamp;
  for (const res of run._subscribers) {
    if (!res.writableEnded) writeSSE(res, event);
  }
}

function setStatus(run: Run, status: RunStatus): void {
  run.status = status;
  emit(run, "status", { status });
}

function writeSSE(res: ServerResponse, event: RunEvent): void {
  // `id:` lets EventSource resume via Last-Event-ID; clients can also pass
  // ?since= on reconnect. `event:` carries the type for addEventListener.
  res.write(`id: ${event.seq}\n`);
  res.write(`event: ${event.type}\n`);
  res.write(`data: ${JSON.stringify(event)}\n\n`);
}

// ── Run execution ──────────────────────────────────────────────────────────

function startRun(skill: string, varValue: string): Run {
  const now = new Date().toISOString();
  const run: Run = {
    id: randomUUID(),
    skill,
    var: varValue,
    status: "queued",
    createdAt: now,
    updatedAt: now,
    result: null,
    error: null,
    events: [],
    _seq: 0,
    _subscribers: new Set(),
    _abort: new AbortController(),
  };
  runs.set(run.id, run);
  evictStaleRuns();

  emit(run, "status", { status: "queued" });

  // Kick off async; the POST returns immediately with the queued run.
  setImmediate(() => execute(run));
  return run;
}

function execute(run: Run): void {
  setStatus(run, "running");
  process.stderr.write(
    `[aeon-rest] run ${run.id} skill=${run.skill}${run.var ? ` var=${run.var}` : ""}\n`
  );

  runPrompt(buildSkillPrompt(run.skill, run.var), defaultPlan(), {
    cwd: REPO_ROOT,
    signal: run._abort.signal,
    onProgress: (ev) => {
      // Don't echo raw event bodies wholesale; surface the useful fields.
      emit(run, ev.kind, {
        ...(ev.text !== undefined ? { text: ev.text } : {}),
        ...(ev.tool !== undefined ? { tool: ev.tool } : {}),
      });
    },
    onFailure: ({ index, target, error }) =>
      process.stderr.write(
        `[aeon-rest] run ${run.id} attempt ${index + 1} (${target.model}@${target.gateway ?? "direct"}) failed: ${error}\n`
      ),
  })
    .then((result) => {
      if (run.status === "canceled") return; // cancel already settled the run
      if (result.ok) {
        run.result = result.output;
        finalize(run, "completed");
      } else {
        run.error = result.error;
        finalize(run, "failed");
      }
    })
    .catch((err: unknown) => {
      if (run.status === "canceled") return;
      run.error = err instanceof Error ? err.message : String(err);
      finalize(run, "failed");
    });
}

function finalize(run: Run, status: RunStatus): void {
  run._completedAt = Date.now();
  emit(run, "status", {
    status,
    ...(run.result !== null ? { result: run.result } : {}),
    ...(run.error !== null ? { error: run.error } : {}),
  });
  run.status = status;
  for (const res of run._subscribers) {
    if (!res.writableEnded) {
      res.write("event: done\ndata: {}\n\n");
      res.end();
    }
  }
  run._subscribers.clear();
}

// ── Serialization ──────────────────────────────────────────────────────────

function serializeRun(run: Run): Record<string, unknown> {
  return {
    id: run.id,
    skill: run.skill,
    var: run.var,
    status: run.status,
    createdAt: run.createdAt,
    updatedAt: run.updatedAt,
    result: run.result,
    error: run.error,
    eventCount: run.events.length,
  };
}

// ── HTTP plumbing ──────────────────────────────────────────────────────────

const CORS_HEADERS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type, Authorization",
};

const MAX_BODY_BYTES = 1024 * 1024;

function json(res: ServerResponse, status: number, data: unknown): void {
  res.writeHead(status, { "Content-Type": "application/json", ...CORS_HEADERS });
  res.end(JSON.stringify(data));
}

function readBody(req: IncomingMessage): Promise<string> {
  return new Promise((resolve, reject) => {
    const chunks: Buffer[] = [];
    let size = 0;
    req.on("data", (chunk: Buffer) => {
      size += chunk.length;
      if (size > MAX_BODY_BYTES) {
        req.destroy();
        reject(new Error("Request body too large"));
        return;
      }
      chunks.push(chunk);
    });
    req.on("end", () => resolve(Buffer.concat(chunks).toString("utf-8")));
    req.on("error", reject);
  });
}

/**
 * Handle a request if it targets the REST API. Returns true when handled,
 * false to let the caller fall through to other routers (A2A, agent card).
 */
export async function handleRestRequest(
  req: IncomingMessage,
  res: ServerResponse,
  url: URL
): Promise<boolean> {
  const path = url.pathname;
  if (!path.startsWith("/api/v1/")) return false;
  const method = req.method ?? "GET";
  const rest = path.slice("/api/v1".length); // e.g. "/runs/123/events"

  // GET /skills
  if (method === "GET" && rest === "/skills") {
    json(res, 200, { skills: getSkills() });
    return true;
  }

  // GET /skills/:slug
  const skillMatch = rest.match(/^\/skills\/([a-z0-9-]+)$/i);
  if (method === "GET" && skillMatch) {
    const skill = getSkillBySlug(skillMatch[1].toLowerCase());
    if (!skill) {
      json(res, 404, { error: `Skill not found: ${skillMatch[1]}` });
      return true;
    }
    json(res, 200, skill);
    return true;
  }

  // POST /runs
  if (method === "POST" && rest === "/runs") {
    let body: string;
    try {
      body = await readBody(req);
    } catch {
      json(res, 400, { error: "Cannot read request body" });
      return true;
    }
    let parsed: { skill?: string; slug?: string; var?: string };
    try {
      parsed = body ? JSON.parse(body) : {};
    } catch {
      json(res, 400, { error: "Invalid JSON" });
      return true;
    }
    const slugRaw = parsed.skill ?? parsed.slug;
    const slug = typeof slugRaw === "string" ? slugRaw.replace(/^aeon-/, "").toLowerCase() : "";
    if (!slug || !getSkillBySlug(slug)) {
      json(res, 400, {
        error: 'Missing or unknown "skill". Pass a valid skill slug.',
        examples: getSkills().slice(0, 5).map((s) => s.slug),
      });
      return true;
    }
    if (!skillFileExists(slug)) {
      json(res, 404, { error: `Skill '${slug}' has no SKILL.md on disk` });
      return true;
    }
    const run = startRun(slug, typeof parsed.var === "string" ? parsed.var : "");
    res.writeHead(201, {
      "Content-Type": "application/json",
      Location: `/api/v1/runs/${run.id}`,
      ...CORS_HEADERS,
    });
    res.end(JSON.stringify(serializeRun(run)));
    return true;
  }

  // GET /runs
  if (method === "GET" && rest === "/runs") {
    const list = [...runs.values()]
      .sort((a, b) => b.createdAt.localeCompare(a.createdAt))
      .map(serializeRun);
    json(res, 200, { runs: list });
    return true;
  }

  // /runs/:id and sub-resources
  const runMatch = rest.match(/^\/runs\/([^/]+)(\/events|\/stream|\/cancel)?$/);
  if (runMatch) {
    const run = runs.get(runMatch[1]);
    const sub = runMatch[2];

    if (!run) {
      json(res, 404, { error: `Run not found: ${runMatch[1]}` });
      return true;
    }

    // GET /runs/:id
    if (method === "GET" && !sub) {
      json(res, 200, serializeRun(run));
      return true;
    }

    // GET /runs/:id/events?since=N
    if (method === "GET" && sub === "/events") {
      const since = parseInt(url.searchParams.get("since") ?? "0", 10) || 0;
      const events = run.events.filter((e) => e.seq > since);
      json(res, 200, { id: run.id, status: run.status, since, events });
      return true;
    }

    // POST /runs/:id/cancel
    if (method === "POST" && sub === "/cancel") {
      if (run.status === "queued" || run.status === "running") {
        run._abort.abort();
        run.error = "Canceled by caller.";
        finalize(run, "canceled");
      }
      json(res, 200, serializeRun(run));
      return true;
    }

    // GET /runs/:id/stream — SSE
    if (method === "GET" && sub === "/stream") {
      res.writeHead(200, {
        "Content-Type": "text/event-stream",
        "Cache-Control": "no-cache",
        Connection: "keep-alive",
        "X-Accel-Buffering": "no",
        ...CORS_HEADERS,
      });

      // Replay backlog after the client's resume point, then attach live.
      const lastEventId = parseInt(
        (req.headers["last-event-id"] as string) ?? url.searchParams.get("since") ?? "0",
        10
      ) || 0;
      for (const event of run.events) {
        if (event.seq > lastEventId) writeSSE(res, event);
      }

      // If already finished, close after replaying — nothing more will come.
      if (run.status === "completed" || run.status === "failed" || run.status === "canceled") {
        res.write("event: done\ndata: {}\n\n");
        res.end();
        return true;
      }

      run._subscribers.add(res);
      const keepAlive = setInterval(() => {
        if (!res.writableEnded) res.write(": keep-alive\n\n");
      }, 15000);
      req.on("close", () => {
        clearInterval(keepAlive);
        run._subscribers.delete(res);
      });
      return true;
    }
  }

  json(res, 404, { error: "Not found" });
  return true;
}
