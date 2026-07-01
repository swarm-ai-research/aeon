# shared/

Canonical sources for code that must run identically across the independent TS
packages (`mcp-server`, `a2a-server`). Aeon isn't a workspace monorepo, so we
distribute via copy rather than runtime imports.

## Files
- `llm-runner.ts` — provider-aware LLM invocation with primary + fallback chain.
  Today only the `claude` CLI transport is implemented; the `LlmProvider` enum
  is the extension point for future SDKs (OpenAI, Gemini, etc.). Pass
  `RunOptions.onProgress` to stream live `ProgressEvent`s (the runner switches
  to `claude --output-format stream-json`); omit it for the buffered path.

## Editing
1. Edit the file under `shared/`.
2. Run `scripts/sync-llm-runner.sh` from the repo root to copy into each
   consumer's `src/`.
3. Commit the canonical source and the regenerated copies together.

## Runtime config

Both callers (`mcp-server`, `a2a-server`) read these env vars at request time:

| Var | Default | Meaning |
|-----|---------|---------|
| `AEON_LLM_MODEL` | `claude-opus-4-7` | Primary model passed to `claude --model`. |
| `AEON_LLM_GATEWAY` | `direct` | Primary gateway: `direct` (ANTHROPIC_API_KEY) or `bankr` (ANTHROPIC_BASE_URL=llm.bankr.bot + BANKR_LLM_KEY). |
| `ANTHROPIC_API_KEY` | — | Used when gateway is `direct`. |
| `BANKR_LLM_KEY` | — | Used when gateway is `bankr`. |

Fallback behavior: if a `direct` primary fails and `BANKR_LLM_KEY` is present,
the runner retries via the `bankr` gateway. Vice versa for `bankr` → `direct`.

## Why not a shared package?

Each TS app has its own `package.json` + `tsconfig.json` with no workspace root.
Adding pnpm/turbo workspaces would be a bigger change than is warranted today.
The copy pattern keeps each app deployable as-is.
