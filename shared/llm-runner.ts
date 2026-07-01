/* Canonical source. Do not edit copies in mcp-server/src/ or a2a-server/src/.
 * Run scripts/sync-llm-runner.sh to propagate changes. */

import { spawn } from "child_process";

export type LlmProvider = "claude";

export type LlmGateway = "direct" | "bankr";

export interface LlmTarget {
  provider: LlmProvider;
  model: string;
  gateway?: LlmGateway;
}

export interface LlmPlan {
  primary: LlmTarget;
  fallbacks?: LlmTarget[];
}

/**
 * A live progress event emitted while a skill runs. Mirrors the salient
 * `claude --output-format stream-json` NDJSON event types, normalized so HTTP
 * SSE callers don't need to know the CLI wire format.
 */
export interface ProgressEvent {
  /** Normalized event kind. `raw` carries any line we couldn't classify. */
  kind: "init" | "assistant" | "tool_use" | "tool_result" | "result" | "raw";
  /** Human-readable text payload (assistant text, tool name, final result). */
  text?: string;
  /** Tool name for `tool_use` / `tool_result` events. */
  tool?: string;
  /** The underlying parsed CLI event, for callers that want full fidelity. */
  raw?: unknown;
}

export interface RunOptions {
  timeoutMs?: number;
  maxBufferBytes?: number;
  signal?: AbortSignal;
  /** Working directory for the spawned claude process. Skills reference
   * `skills/${slug}/SKILL.md` via relative paths, so callers should pass the
   * repo root here regardless of where the server process was launched. */
  cwd?: string;
  onAttempt?: (attempt: { index: number; target: LlmTarget }) => void;
  onFailure?: (failure: {
    index: number;
    target: LlmTarget;
    error: string;
  }) => void;
  /**
   * When set, the run streams live progress. The runner spawns claude with
   * `--output-format stream-json` and invokes this for each emitted event.
   * When unset, the buffered `--output-format json` path is used (no progress).
   */
  onProgress?: (event: ProgressEvent) => void;
}

export interface RunSuccess {
  ok: true;
  output: string;
  target: LlmTarget;
  attempts: number;
}

export interface RunFailure {
  ok: false;
  error: string;
  attempts: Array<{ target: LlmTarget; error: string }>;
}

export type RunResult = RunSuccess | RunFailure;

const DEFAULT_TIMEOUT_MS = 600_000; // 10 minutes — matches GitHub Actions skill timeout
const DEFAULT_MAX_BUFFER = 10 * 1024 * 1024; // 10 MB

export async function runPrompt(
  prompt: string,
  plan: LlmPlan,
  opts: RunOptions = {}
): Promise<RunResult> {
  const targets = [plan.primary, ...(plan.fallbacks ?? [])];
  const failures: Array<{ target: LlmTarget; error: string }> = [];

  for (let i = 0; i < targets.length; i++) {
    if (opts.signal?.aborted) {
      failures.push({ target: targets[i], error: "aborted before attempt" });
      break;
    }
    const target = targets[i];
    opts.onAttempt?.({ index: i, target });

    const attempt = await runOnce(prompt, target, opts);
    if (attempt.ok) {
      return { ok: true, output: attempt.output, target, attempts: i + 1 };
    }
    failures.push({ target, error: attempt.error });
    opts.onFailure?.({ index: i, target, error: attempt.error });
    // If the abort signal fired, don't keep trying fallbacks.
    if (opts.signal?.aborted) break;
  }

  return {
    ok: false,
    error: failures.map((f) => `${describe(f.target)}: ${f.error}`).join(" | "),
    attempts: failures,
  };
}

interface OnceOk {
  ok: true;
  output: string;
}
interface OnceErr {
  ok: false;
  error: string;
}

async function runOnce(
  prompt: string,
  target: LlmTarget,
  opts: RunOptions
): Promise<OnceOk | OnceErr> {
  switch (target.provider) {
    case "claude":
      return runClaudeCli(prompt, target, opts);
    default:
      // Exhaustive switch — adding a new LlmProvider variant will surface here.
      return {
        ok: false,
        error: `Unsupported provider: ${(target as { provider: string }).provider}`,
      };
  }
}

async function runClaudeCli(
  prompt: string,
  target: LlmTarget,
  opts: RunOptions
): Promise<OnceOk | OnceErr> {
  const env = claudeEnv(target.gateway ?? "direct");
  const timeoutMs = opts.timeoutMs ?? DEFAULT_TIMEOUT_MS;
  const maxBuffer = opts.maxBufferBytes ?? DEFAULT_MAX_BUFFER;
  const streaming = typeof opts.onProgress === "function";

  // stream-json emits one JSON event per line as the agent works; json buffers
  // a single result object. We only pay the streaming parse cost when a caller
  // actually wants progress.
  const args = streaming
    ? ["-p", "-", "--output-format", "stream-json", "--verbose", "--model", target.model]
    : ["-p", "-", "--output-format", "json", "--model", target.model];

  return new Promise<OnceOk | OnceErr>((resolve) => {
    const child = spawn("claude", args, { env, cwd: opts.cwd, stdio: ["pipe", "pipe", "pipe"] });

    let stdout = "";
    let stderr = "";
    let truncated = false;
    let settled = false;
    // For streaming: incomplete trailing line carried between data chunks, and
    // the final result text extracted from the terminal `result` event.
    let lineBuffer = "";
    let streamedResult: string | null = null;
    let assistantText = "";

    const settle = (result: OnceOk | OnceErr) => {
      if (settled) return;
      settled = true;
      clearTimeout(timer);
      resolve(result);
    };

    const timer = setTimeout(() => {
      child.kill("SIGKILL");
      settle({ ok: false, error: `claude timed out after ${timeoutMs}ms` });
    }, timeoutMs);

    const onAbort = () => {
      child.kill("SIGTERM");
      settle({ ok: false, error: "aborted by caller" });
    };
    if (opts.signal) {
      if (opts.signal.aborted) {
        onAbort();
      } else {
        opts.signal.addEventListener("abort", onAbort, { once: true });
      }
    }

    const handleStreamLine = (line: string) => {
      const trimmed = line.trim();
      if (!trimmed) return;
      let event: unknown;
      try {
        event = JSON.parse(trimmed);
      } catch {
        opts.onProgress?.({ kind: "raw", text: trimmed, raw: trimmed });
        return;
      }
      const progress = normalizeStreamEvent(event);
      if (progress) {
        if (progress.kind === "assistant" && progress.text) {
          assistantText += progress.text;
        }
        if (progress.kind === "result" && typeof progress.text === "string") {
          streamedResult = progress.text;
        }
        opts.onProgress?.(progress);
      }
    };

    child.stdout.on("data", (chunk: Buffer) => {
      if (truncated) return;
      const str = chunk.toString("utf-8");
      stdout += str;
      if (stdout.length > maxBuffer) {
        truncated = true;
        child.kill("SIGKILL");
        settle({ ok: false, error: `stdout exceeded ${maxBuffer} bytes` });
        return;
      }
      if (streaming) {
        lineBuffer += str;
        let nl: number;
        while ((nl = lineBuffer.indexOf("\n")) !== -1) {
          handleStreamLine(lineBuffer.slice(0, nl));
          lineBuffer = lineBuffer.slice(nl + 1);
        }
      }
    });
    child.stderr.on("data", (chunk: Buffer) => {
      stderr += chunk.toString("utf-8");
    });

    child.on("error", (err: NodeJS.ErrnoException) => {
      const msg =
        err.code === "ENOENT"
          ? "'claude' command not found (install with: npm install -g @anthropic-ai/claude-code)"
          : `failed to spawn claude: ${err.message}`;
      settle({ ok: false, error: msg });
    });

    child.on("close", (code: number | null) => {
      if (code === 0) {
        if (streaming) {
          if (lineBuffer.trim()) handleStreamLine(lineBuffer);
          // Prefer the explicit result event; fall back to concatenated
          // assistant text if the stream ended without one.
          settle({ ok: true, output: streamedResult ?? assistantText.trim() });
        } else {
          settle({ ok: true, output: parseClaudeJsonOutput(stdout.trim()) });
        }
      } else {
        const detail = (stderr || stdout).trim().slice(-2000);
        settle({ ok: false, error: `exit ${code ?? "null"}: ${detail}` });
      }
    });

    child.stdin.write(prompt);
    child.stdin.end();
  });
}

/**
 * Map a parsed `stream-json` NDJSON event to a normalized ProgressEvent.
 * Returns null for events we intentionally drop (e.g. user/tool-result echoes
 * with no useful surface). Defensive about shape — the CLI wire format is not
 * a stable contract.
 */
function normalizeStreamEvent(event: unknown): ProgressEvent | null {
  if (!event || typeof event !== "object") return null;
  const e = event as Record<string, unknown>;
  const type = e.type;

  if (type === "system" && e.subtype === "init") {
    return { kind: "init", raw: event };
  }

  if (type === "result") {
    const result = typeof e.result === "string" ? e.result : "";
    return { kind: "result", text: result, raw: event };
  }

  if (type === "assistant" || type === "user") {
    const message = e.message as { content?: unknown } | undefined;
    const content = Array.isArray(message?.content) ? message!.content : [];
    let text = "";
    let toolName: string | undefined;
    let kind: ProgressEvent["kind"] = type === "assistant" ? "assistant" : "tool_result";
    for (const block of content as Array<Record<string, unknown>>) {
      if (block.type === "text" && typeof block.text === "string") {
        text += block.text;
      } else if (block.type === "tool_use") {
        kind = "tool_use";
        if (typeof block.name === "string") toolName = block.name;
      } else if (block.type === "tool_result") {
        kind = "tool_result";
      }
    }
    if (!text && !toolName && kind !== "tool_result") return null;
    return { kind, text: text || undefined, tool: toolName, raw: event };
  }

  return null;
}

function claudeEnv(gateway: LlmGateway): NodeJS.ProcessEnv {
  // Inherit current env, then layer gateway-specific overrides. We deliberately
  // mutate a shallow copy so the parent process env isn't touched.
  const env: NodeJS.ProcessEnv = { ...process.env };

  if (gateway === "bankr") {
    const key = process.env.BANKR_LLM_KEY;
    if (!key) {
      // Don't throw — let the spawn fail with a clear error so callers can
      // fall back to the next target.
    }
    env.ANTHROPIC_BASE_URL = "https://llm.bankr.bot";
    env.ANTHROPIC_AUTH_TOKEN = key ?? "";
    delete env.ANTHROPIC_API_KEY;
  } else {
    delete env.ANTHROPIC_BASE_URL;
    delete env.ANTHROPIC_AUTH_TOKEN;
  }

  return env;
}

function parseClaudeJsonOutput(stdout: string): string {
  if (!stdout) return "";
  try {
    const parsed = JSON.parse(stdout) as { result?: string };
    return parsed.result ?? stdout;
  } catch {
    return stdout;
  }
}

function describe(t: LlmTarget): string {
  return `${t.provider}/${t.model}${t.gateway && t.gateway !== "direct" ? `@${t.gateway}` : ""}`;
}
