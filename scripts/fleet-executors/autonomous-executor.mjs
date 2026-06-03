/**
 * autonomous-executor.mjs — Generic autonomous execution harness.
 *
 * Wires all building blocks into a single `executeAutonomously()` call:
 *   1. WakeUpStack — assembles tiered context (L0 identity + L1 essentials + L2 on-demand)
 *   2. SignalActionMap — constrains available actions per signal type
 *   3. ContentSafety — sanitizes external input before LLM interpolation
 *   4. GoalLoop — step-by-step execution with self-correction
 *   5. DoomLoop — integrated into GoalLoop, catches stuck agents
 *
 * Usage:
 *   import { executeAutonomously } from "./autonomous-executor.mjs";
 *
 *   const result = await executeAutonomously({
 *     goal: "Research the top 3 JavaScript ORMs",
 *     signalType: "manual_trigger",
 *     identity: { role: "researcher", domains: ["javascript", "databases"] },
 *     inference: async ({ systemPrompt, userPrompt }) => {
 *       // Call your LLM here
 *       return { content: "..." };
 *     },
 *     executeAction: async ({ actionName, actionParams }) => {
 *       // Execute the action (git, web search, file I/O, etc.)
 *       return { output: "...", cost: 0 };
 *     },
 *     retrieveEssentials: async () => [{ text: "...", score: 0.9 }],
 *     retrieveOnDemand: async (query) => [{ text: "...", score: 0.8 }],
 *   });
 *
 *   // result.outcome — "complete" | "blocked_stuck" | "blocked_capability"
 *   // result.artifact — { title, body, description }
 *   // result.stepsExecuted — number of steps taken
 *   // result.context — { l0, l1, l2 } — what context was assembled
 */

import { GoalLoop, GOAL_STEP_SYSTEM_PROMPT } from "./goal-loop.mjs";
import { getActionsForSignal, buildActionPromptSection, getSelectionMode } from "./signal-action-map.mjs";
import { sanitize, assessThreat, extractSafeText, UNTRUSTED_CONTENT_INSTRUCTION } from "./content-safety.mjs";
import { WakeUpStack } from "./wake-up-stack.mjs";

/**
 * @typedef {Object} AutonomousOptions
 * @property {string} goal — What to accomplish
 * @property {string} [signalType="manual_trigger"] — What triggered this
 * @property {{ role: string, domains: string[] }} identity — Agent identity
 * @property {Function} inference — async ({ systemPrompt, userPrompt, maxTokens, temperature }) => { content }
 * @property {Function} executeAction — async ({ actionName, actionParams }) => { output, cost? }
 * @property {Function} [retrieveEssentials] — async () => KnowledgeItem[]
 * @property {Function} [retrieveOnDemand] — async (query, mode) => KnowledgeItem[]
 * @property {number} [budgetCredits=1000] — Soft budget cap
 * @property {number} [maxSteps=20] — Hard step limit
 * @property {boolean} [verbose=false] — Log progress
 * @property {Function} [onStep] — Callback after each step
 * @property {string[]} [extraCategories] — Extra action categories to include
 * @property {string} [untrustedInput] — External input to sanitize (e.g., from another agent)
 */

/**
 * Execute a goal autonomously using all building blocks.
 *
 * @param {AutonomousOptions} options
 * @returns {Promise<Object>} Result with outcome, artifact, stepsExecuted, context
 */
export async function executeAutonomously(options) {
  const {
    goal,
    signalType = "manual_trigger",
    identity,
    inference,
    executeAction,
    retrieveEssentials,
    retrieveOnDemand,
    budgetCredits = 1000,
    maxSteps = 20,
    verbose = false,
    onStep,
    extraCategories = [],
    untrustedInput,
  } = options;

  const log = verbose ? console.log : () => {};

  // ── 1. Wake-Up Stack: assemble context ─────────────────────
  log("[autonomous] assembling context...");

  const stack = new WakeUpStack({
    identity,
    retrieveEssentials: retrieveEssentials || (async () => []),
    retrieveOnDemand: retrieveOnDemand || (async () => []),
    verbose,
  });

  const selectionMode = getSelectionMode(signalType);
  const context = await stack.getContext(goal, selectionMode);

  log(`[autonomous] context: L0=${context.l0.length} chars, L1=${context.l1.length} items, L2=${context.l2.length} items`);

  // ── 2. Signal-Action Map: get available actions ─────────────
  const actions = getActionsForSignal(signalType, { extraCategories });
  const actionPrompt = buildActionPromptSection(signalType, { extraCategories });

  log(`[autonomous] ${actions.length} actions available for signal "${signalType}"`);

  // ── 3. Content Safety: sanitize external input ─────────────
  let safeInputSection = "";
  if (untrustedInput) {
    const threat = assessThreat(untrustedInput);
    if (threat.level !== "safe") {
      log(`[autonomous] threat detected: ${threat.level} (${threat.matches.length} matches)`);
    }
    safeInputSection = [
      "",
      "## External Input (untrusted)",
      // The explicit instruction is the core injection defense — the wrapper
      // tags alone are weaker without it.
      UNTRUSTED_CONTENT_INSTRUCTION,
      extractSafeText(untrustedInput, "external input"),
      "",
    ].join("\n");
  }

  // ── 4. Build enriched system prompt ────────────────────────
  const systemPrompt = [
    GOAL_STEP_SYSTEM_PROMPT.replace("{maxSteps}", String(maxSteps)),
    "",
    "## Your Context",
    context.markdown,
    "",
    actionPrompt,
    safeInputSection,
  ].join("\n");

  // ── 5. Goal Loop: execute step-by-step ─────────────────────
  log("[autonomous] starting goal loop...");

  const result = await GoalLoop.run({
    goal,
    budgetCredits,
    maxSteps,
    verbose,
    onStep,
    inference: async ({ userPrompt, maxTokens, temperature }) => {
      // Inject context into user prompt
      const enrichedPrompt = [
        context.l2.length > 0 ? `## Relevant Context\n${context.l2.map(i => `- ${i.text}`).join("\n")}` : "",
        userPrompt,
      ].filter(Boolean).join("\n\n");

      return inference({
        systemPrompt,
        userPrompt: enrichedPrompt,
        maxTokens: maxTokens || 1024,
        temperature: temperature ?? 0.5,
      });
    },
    executeAction: async ({ actionName, actionParams }) => {
      // Validate action is in the allowed set
      if (!actions.includes(actionName) && actionName !== "browse_tools") {
        return {
          output: `error: action '${actionName}' is not available for signal '${signalType}'. Available: ${actions.join(", ")}`,
          cost: 0,
        };
      }

      // Execute with content safety for external results
      const execResult = await executeAction({ actionName, actionParams });

      // Sanitize output if it came from an external source
      if (execResult.output && typeof execResult.output === "string") {
        const threat = assessThreat(execResult.output);
        if (threat.level === "high" || threat.level === "critical") {
          log(`[autonomous] high-threat output from ${actionName}, sanitizing`);
          execResult.output = sanitize(execResult.output);
        }
      }

      return execResult;
    },
  });

  // ── 6. Return enriched result ──────────────────────────────
  return {
    ...result,
    context: {
      l0: context.l0,
      l1: context.l1,
      l2: context.l2,
    },
    actionsUsed: actions,
    signalType,
  };
}

/**
 * Create an executor function bound to a specific agent identity.
 * Useful for registering in the fleet runner config.
 *
 * @param {Object} agentConfig
 * @param {string} agentConfig.name — Agent name
 * @param {{ role: string, domains: string[] }} agentConfig.identity
 * @param {Function} agentConfig.inference — LLM function
 * @param {Function} agentConfig.executeAction — Action executor
 * @param {Object} [agentConfig.opts] — Default options
 * @returns {Function} async (goal, signalType?, extraOpts?) => result
 */
export function createAgent(agentConfig) {
  const { name, identity, inference, executeAction, opts = {} } = agentConfig;

  return async function run(goal, signalType = "manual_trigger", extraOpts = {}) {
    console.log(`[${name}] executing: ${goal.slice(0, 80)}`);

    const result = await executeAutonomously({
      goal,
      signalType,
      identity,
      inference,
      executeAction,
      ...opts,
      ...extraOpts,
    });

    console.log(`[${name}] ${result.outcome}: ${result.stepsExecuted} steps, ${result.creditsSpent} credits`);
    return result;
  };
}

export default { executeAutonomously, createAgent };
