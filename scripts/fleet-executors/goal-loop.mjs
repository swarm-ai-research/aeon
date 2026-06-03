/**
 * goal-loop.mjs — Step-by-step autonomous execution engine for goal-driven agents.
 *
 * Ported from Nookplot's goal_loop.py. An LLM takes a goal, breaks it into
 * steps, and executes them one at a time. The loop detects stuck states,
 * doom loops, and budget overruns.
 *
 * Termination outcomes:
 *   - "complete"          — goal achieved (or max-steps/no-op fallback returns
 *                           what was accomplished so far)
 *   - "blocked_stuck"     — 3x same description, doom loop, or 3x no-ops
 *   - "blocked_capability" — agent declared it can't do this
 *
 * The step budget is a soft cap: exceeding it logs a warning and the loop
 * returns a "complete" fallback artifact rather than a distinct outcome.
 *
 * Usage:
 *   import { GoalLoop } from "./goal-loop.mjs";
 *
 *   const result = await GoalLoop.run({
 *     goal: "Research the top 3 JavaScript ORMs and compare them",
 *     budgetCredits: 100,
 *     maxSteps: 20,
 *     inference: async ({ systemPrompt, userPrompt, maxTokens }) => {
 *       // Call your LLM here (Claude, GPT-4, Ollama, etc.)
 *       return { content: "..." };
 *     },
 *     executeAction: async ({ actionName, actionParams }) => {
 *       // Execute the action and return output
 *       return { output: "...", cost: 0 };
 *     },
 *   });
 */

import { DoomLoopDetector, buildCorrectivePrompt } from "./doom-loop.mjs";

// ── Constants ────────────────────────────────────────────────

const DEFAULT_MAX_STEPS = 20;
const DEFAULT_MAX_CONSECUTIVE_NOOPS = 3;
const DEFAULT_MAX_REFORMULATIONS = 3;
const DEFAULT_BUDGET = 1000;
const DOOM_LOOP_MAX_TRIGGERS = 3;

// ── System prompt ────────────────────────────────────────────

export const GOAL_STEP_SYSTEM_PROMPT = `You are an autonomous agent working on a specific goal. Each turn, you choose the single next action that moves you toward completion.

Your decision each turn is ONE of:

1. Execute an action — return { "type": "action", "action_name": "...", "action_params": {...}, "description": "..." }
2. Complete the goal — return { "type": "complete", "title": "...", "body": "<final markdown artifact>", "description": "..." }
3. Declare no-op — return { "type": "noop", "description": "..." }  (use sparingly; 3 consecutive no-ops ends the goal)
4. Declare capability gap — return { "type": "needs_capability", "description": "..." }

Rules:
- Be concise and focused. Do NOT explore beyond the goal.
- You have a hard cap of {maxSteps} steps. Do not waste them.
- If the goal is ambiguous, interpret narrowly — complete a narrow version rather than wandering broadly.
- Budget is a soft cap — stay under if you can, but the goal matters more than the cost.
- When finished, ALWAYS return type "complete" with the deliverable in "body". Do NOT keep iterating after the goal is achieved.

Return only valid JSON. No prose outside the JSON block.`;

// ── Decision parsing ─────────────────────────────────────────

const JSON_BLOCK_RE = /\{[\s\S]*\}/;

/**
 * Parse a goal action from an LLM response.
 * Tolerant to prose wrapping the JSON block.
 *
 * @param {string} content - LLM response text
 * @returns {Object|null} Parsed decision or null
 */
export function parseGoalAction(content) {
  if (!content || typeof content !== "string") return null;

  const match = content.match(JSON_BLOCK_RE);
  if (!match) return null;

  let parsed;
  try {
    parsed = JSON.parse(match[0]);
  } catch {
    return null;
  }
  if (typeof parsed !== "object" || parsed === null) return null;

  const { type } = parsed;
  if (typeof type !== "string") return null;

  if (type === "action") {
    const actionName = parsed.action_name;
    if (typeof actionName !== "string" || !actionName) return null;
    return {
      type: "action",
      action_name: actionName,
      action_params: typeof parsed.action_params === "object" ? parsed.action_params : {},
      description: typeof parsed.description === "string" ? parsed.description : actionName,
    };
  }

  if (type === "complete") {
    const { title, body } = parsed;
    if (typeof title !== "string" || !title || typeof body !== "string" || !body) return null;
    return {
      type: "complete",
      title,
      body,
      description: typeof parsed.description === "string" ? parsed.description : "complete",
    };
  }

  if (type === "noop") {
    return {
      type: "noop",
      description: typeof parsed.description === "string" ? parsed.description : "noop",
    };
  }

  if (type === "needs_capability") {
    const description = parsed.description;
    if (typeof description !== "string" || !description) return null;
    return {
      type: "needs_capability",
      description,
      suggested_preset: typeof parsed.suggested_preset === "string" ? parsed.suggested_preset : null,
    };
  }

  return null;
}

// ── Prompt builder ───────────────────────────────────────────

/**
 * Build the per-step user prompt for the LLM.
 *
 * @param {string} goal - The goal description
 * @param {Array} previousSteps - Steps executed so far
 * @param {number} spentCredits - Credits spent so far
 * @param {number} budgetCredits - Soft budget cap
 * @returns {string}
 */
export function buildStepPrompt(goal, previousSteps, spentCredits, budgetCredits) {
  const stepsText = previousSteps.length === 0
    ? "(no previous steps)"
    : previousSteps
        .slice(-8)
        .map((s, i) => `${i + 1}. ${s.action_type || "?"}: ${(s.output_summary || "").slice(0, 180)}`)
        .join("\n");

  return [
    `Goal: ${goal}`,
    "",
    `Previous steps:\n${stepsText}`,
    "",
    `Spent so far: ${spentCredits} / ${budgetCredits} credits (soft cap)`,
    "",
    "Choose the next action. Return JSON only.",
  ].join("\n");
}

// ── GoalLoop ─────────────────────────────────────────────────

/**
 * @typedef {Object} GoalResult
 * @property {"complete"|"blocked_stuck"|"blocked_capability"} outcome
 * @property {number} stepsExecuted
 * @property {number} creditsSpent
 * @property {Object|null} [artifact] - For "complete" outcome: { title, body, description }
 * @property {string|null} [stuckReason] - For "blocked_stuck" outcome
 * @property {string|null} [capabilityNeeded] - For "blocked_capability" outcome
 */

/**
 * @typedef {Object} GoalLoopOptions
 * @property {string} goal - What to accomplish
 * @property {Function} inference - async ({ systemPrompt, userPrompt, maxTokens, temperature }) => { content }
 * @property {Function} executeAction - async ({ actionName, actionParams }) => { output, cost? }
 * @property {number} [budgetCredits=1000] - Soft budget cap
 * @property {number} [maxSteps=20] - Hard step limit
 * @property {number} [maxConsecutiveNoops=3] - No-op limit before fallback
 * @property {number} [maxReformulations=3] - Same-description limit before stuck
 * @property {boolean} [verbose=false] - Log progress
 * @property {Function} [onStep] - Callback after each step: ({ step, decision, output }) => void
 */

export class GoalLoop {
  /**
   * Run a goal loop to completion.
   *
   * @param {GoalLoopOptions} options
   * @returns {Promise<GoalResult>}
   */
  static async run(options) {
    const {
      goal,
      inference,
      executeAction,
      budgetCredits = DEFAULT_BUDGET,
      maxSteps = DEFAULT_MAX_STEPS,
      maxConsecutiveNoops = DEFAULT_MAX_CONSECUTIVE_NOOPS,
      maxReformulations = DEFAULT_MAX_REFORMULATIONS,
      verbose = false,
      onStep,
    } = options;

    const recentSteps = [];
    let spentCredits = 0;
    let stepsExecuted = 0;
    let consecutiveNoops = 0;
    let sameStepRepetitions = 0;
    let lastStepDescription = "";

    // Doom loop tracking
    const doomDetector = new DoomLoopDetector({ lookback: 30, threshold: 3 });
    let doomLoopTriggers = 0;
    let doomLoopNote = null;

    const log = verbose ? console.log : () => {};

    for (let step = 0; step < maxSteps; step++) {
      // ── Ask LLM for next action ──────────────────────────
      const decision = await askForAction({
        goal,
        recentSteps,
        spentCredits,
        budgetCredits,
        maxSteps,
        doomLoopNote,
        inference,
      });

      // Clear doom loop note after injecting it
      if (doomLoopNote) doomLoopNote = null;

      if (decision === null) {
        consecutiveNoops++;
        if (consecutiveNoops >= maxConsecutiveNoops) {
          return finalizeFallback("LLM returned unparseable output 3x", goal, recentSteps, stepsExecuted, spentCredits);
        }
        log(`[goal-loop] step ${step + 1}: unparseable output (${consecutiveNoops}/${maxConsecutiveNoops})`);
        continue;
      }

      const { type: decisionType } = decision;

      // ── Termination: complete ────────────────────────────
      if (decisionType === "complete") {
        return {
          outcome: "complete",
          stepsExecuted,
          creditsSpent: spentCredits,
          artifact: {
            title: decision.title.slice(0, 200),
            body: decision.body.slice(0, 80_000),
            description: decision.description,
          },
          stuckReason: null,
          capabilityNeeded: null,
        };
      }

      // ── Termination: capability gap ──────────────────────
      if (decisionType === "needs_capability") {
        return {
          outcome: "blocked_capability",
          stepsExecuted,
          creditsSpent: spentCredits,
          artifact: null,
          stuckReason: null,
          capabilityNeeded: decision.description.slice(0, 1000),
        };
      }

      // ── Stuck detection (same description) ───────────────
      const description = decision.description || "";
      if (description === lastStepDescription && decisionType !== "noop") {
        sameStepRepetitions++;
        if (sameStepRepetitions >= maxReformulations) {
          return {
            outcome: "blocked_stuck",
            stepsExecuted,
            creditsSpent: spentCredits,
            artifact: null,
            stuckReason: `same step repeated ${maxReformulations}x: ${description.slice(0, 500)}`,
            capabilityNeeded: null,
          };
        }
      } else {
        sameStepRepetitions = 0;
      }
      lastStepDescription = description;

      // ── No-op ────────────────────────────────────────────
      if (decisionType === "noop") {
        consecutiveNoops++;
        if (consecutiveNoops >= maxConsecutiveNoops) {
          return finalizeFallback("agent returned 3 no-ops in a row", goal, recentSteps, stepsExecuted, spentCredits);
        }
        log(`[goal-loop] step ${step + 1}: noop — ${description}`);
        recordStep(recentSteps, step + 1, "noop", description, "");
        continue;
      }
      consecutiveNoops = 0;

      // ── Execute action ───────────────────────────────────
      let execResult;
      try {
        execResult = await executeAction({
          actionName: decision.action_name,
          actionParams: decision.action_params,
        });
      } catch (err) {
        execResult = { output: `error: ${err.message}`.slice(0, 500), cost: 0 };
      }

      const cost = Math.max(0, execResult.cost || 0);
      spentCredits += cost;
      stepsExecuted++;

      const outputSummary = (execResult.output || "").slice(0, 500);
      recordStep(recentSteps, step + 1, decision.action_name, description, outputSummary);

      log(`[goal-loop] step ${step + 1}: ${decision.action_name} — ${description.slice(0, 80)}`);

      // ── Callback ─────────────────────────────────────────
      if (onStep) {
        try {
          onStep({ step: step + 1, decision, output: outputSummary, cost });
        } catch {}
      }

      // ── Doom loop detection ──────────────────────────────
      doomDetector.record(decision.action_name, decision.action_params);
      const doomResult = doomDetector.check();
      if (doomResult) {
        doomLoopTriggers++;
        if (doomLoopTriggers >= DOOM_LOOP_MAX_TRIGGERS) {
          return {
            outcome: "blocked_stuck",
            stepsExecuted,
            creditsSpent: spentCredits,
            artifact: null,
            stuckReason: `doom loop on '${doomResult.offender}' (${doomLoopTriggers} triggers)`,
            capabilityNeeded: null,
          };
        }
        doomLoopNote = doomResult.corrective;
        log(`[goal-loop] doom loop detected: ${doomResult.message} (trigger ${doomLoopTriggers}/${DOOM_LOOP_MAX_TRIGGERS})`);
      }

      // ── Budget warning ───────────────────────────────────
      if (spentCredits > budgetCredits && verbose) {
        console.warn(`[goal-loop] over soft budget: spent=${spentCredits} budget=${budgetCredits}`);
      }
    }

    // Hit max steps
    return finalizeFallback(`hit maxSteps cap (${maxSteps})`, goal, recentSteps, stepsExecuted, spentCredits);
  }
}

// ── Private helpers ──────────────────────────────────────────

async function askForAction({ goal, recentSteps, spentCredits, budgetCredits, maxSteps, doomLoopNote, inference }) {
  try {
    const systemPrompt = GOAL_STEP_SYSTEM_PROMPT.replace("{maxSteps}", String(maxSteps));
    let userPrompt = buildStepPrompt(goal, recentSteps, spentCredits, budgetCredits);

    if (doomLoopNote) {
      userPrompt = `${doomLoopNote}\n\n---\n\n${userPrompt}`;
    }

    const { content } = await inference({
      systemPrompt,
      userPrompt,
      maxTokens: 1024,
      temperature: 0.5,
    });

    return parseGoalAction(content);
  } catch (err) {
    console.error("[goal-loop] inference call failed:", err.message);
    return null;
  }
}

function recordStep(steps, stepNumber, actionType, inputSummary, outputSummary) {
  steps.push({ step_number: stepNumber, action_type: actionType, output_summary: outputSummary });
  if (steps.length > 16) steps.shift();
}

function finalizeFallback(reason, goal, recentSteps, stepsExecuted, spentCredits) {
  let body;
  if (recentSteps.length === 0) {
    body = `Goal loop terminated: ${reason}.\n\nNo progress was made on: ${goal}`;
  } else {
    const stepLines = recentSteps
      .map((s, i) => `${i + 1}. **${s.action_type || "?"}** — ${(s.output_summary || "").slice(0, 200)}`)
      .join("\n");
    body = [
      "# Goal Progress",
      "",
      `**Goal:** ${goal}`,
      "",
      `**Termination:** ${reason}`,
      "",
      `**Steps executed:** ${stepsExecuted}`,
      "",
      `## Recent steps\n\n${stepLines}`,
    ].join("\n");
  }

  return {
    outcome: "complete", // fallback treats as completed-with-what-we-have
    stepsExecuted,
    creditsSpent: spentCredits,
    artifact: {
      title: goal.slice(0, 200),
      body,
      description: `goal-fallback: ${reason}`,
    },
    stuckReason: null,
    capabilityNeeded: null,
  };
}

export default GoalLoop;
