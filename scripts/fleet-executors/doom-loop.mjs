/**
 * doom-loop.mjs — Detect stuck agents that repeat the same actions.
 *
 * Ported from Nookplot's doom_loop.py. Catches two patterns:
 *   1. Identical consecutive: same tool + same args 3+ times in a row
 *   2. Repeating sequence: A→B→A→B cycling (pattern length 2-5, 2+ reps)
 *
 * Usage:
 *   import { DoomLoopDetector } from "./doom-loop.mjs";
 *
 *   const detector = new DoomLoopDetector({ lookback: 30, threshold: 3 });
 *
 *   // Record each action the agent takes
 *   detector.record("git_commit", { message: "fix: typo" });
 *   detector.record("git_commit", { message: "fix: typo" });
 *
 *   const result = detector.check();
 *   if (result) {
 *     console.warn(result.message); // "doom loop: 3+ identical consecutive calls to 'git_commit'"
 *     // Inject corrective guidance or terminate
 *   }
 *
 *   // Or with OpenAI-style messages:
 *   const loop = DoomLoopDetector.fromMessages(messages);
 */

import { createHash } from "node:crypto";

// ── Constants ────────────────────────────────────────────────

const DEFAULT_LOOKBACK = 30;
const IDENTICAL_THRESHOLD = 3;
const MIN_PATTERN_LEN = 2;
const MAX_PATTERN_LEN = 5;
const MIN_PATTERN_REPS = 2;

// ── Helpers ──────────────────────────────────────────────────

function hashArgs(args) {
  const str = typeof args === "string" ? args : JSON.stringify(args, Object.keys(args || {}).sort());
  return createHash("md5").update(str).digest("hex").slice(0, 12);
}

/**
 * @typedef {Object} ToolCallSignature
 * @property {string} name - Tool/action name
 * @property {string} argsHash - Hash of the arguments
 */

/**
 * @typedef {Object} DoomLoopResult
 * @property {string} offender - The tool name causing the loop
 * @property {"identical"|"repeating"} pattern - Type of detected pattern
 * @property {string} message - Human-readable description
 * @property {string} corrective - Prompt to inject for correction
 */

// ── Detector ─────────────────────────────────────────────────

export class DoomLoopDetector {
  /**
   * @param {Object} opts
   * @param {number} [opts.lookback=30] - Max signatures to retain
   * @param {number} [opts.threshold=3] - Identical consecutive calls to trigger
   */
  constructor({ lookback = DEFAULT_LOOKBACK, threshold = IDENTICAL_THRESHOLD } = {}) {
    this.lookback = lookback;
    this.threshold = threshold;
    /** @type {ToolCallSignature[]} */
    this.signatures = [];
  }

  /**
   * Record a tool/action call.
   * @param {string} name - Tool or action name
   * @param {*} [args={}] - Arguments passed (will be JSON-hashed)
   */
  record(name, args = {}) {
    this.signatures.push({ name, argsHash: hashArgs(args) });
    if (this.signatures.length > this.lookback) {
      this.signatures = this.signatures.slice(-this.lookback);
    }
  }

  /**
   * Check for doom loop patterns.
   * @returns {DoomLoopResult|null} Result if loop detected, null otherwise
   */
  check() {
    const sigs = this.signatures;
    if (sigs.length < this.threshold) return null;

    // 1. Identical consecutive
    const identical = this._detectIdentical(sigs);
    if (identical) return identical;

    // 2. Repeating sequence
    const repeating = this._detectRepeating(sigs);
    if (repeating) return repeating;

    return null;
  }

  /**
   * Check and clear if loop detected (convenience for loop bodies).
   * @returns {DoomLoopResult|null}
   */
  checkAndClear() {
    const result = this.check();
    if (result) {
      this.signatures = [];
    }
    return result;
  }

  /**
   * Reset the detector state.
   */
  reset() {
    this.signatures = [];
  }

  // ── Private ──────────────────────────────────────────────

  /** @private */
  _detectIdentical(sigs) {
    let count = 1;
    for (let i = 1; i < sigs.length; i++) {
      if (sigs[i].name === sigs[i - 1].name && sigs[i].argsHash === sigs[i - 1].argsHash) {
        count++;
        if (count >= this.threshold) {
          return {
            offender: sigs[i].name,
            pattern: "identical",
            message: `doom loop: ${this.threshold}+ identical consecutive calls to '${sigs[i].name}'`,
            corrective: buildCorrectivePrompt(sigs[i].name),
          };
        }
      } else {
        count = 1;
      }
    }
    return null;
  }

  /** @private */
  _detectRepeating(sigs) {
    for (let seqLen = MIN_PATTERN_LEN; seqLen <= MAX_PATTERN_LEN; seqLen++) {
      const minRequired = seqLen * MIN_PATTERN_REPS;
      if (sigs.length < minRequired) continue;

      const pattern = sigs.slice(-minRequired, -minRequired + seqLen);
      let reps = 0;

      for (let start = sigs.length - seqLen; start >= 0; start -= seqLen) {
        const chunk = sigs.slice(start, start + seqLen);
        if (chunk.every((s, i) => s.name === pattern[i].name && s.argsHash === pattern[i].argsHash)) {
          reps++;
        } else {
          break;
        }
      }

      if (reps >= MIN_PATTERN_REPS) {
        const desc = pattern.map(s => s.name).join(" → ");
        return {
          offender: pattern[0].name,
          pattern: "repeating",
          message: `doom loop: repeating sequence [${desc}] (${reps} repetitions)`,
          corrective: buildCorrectivePrompt(desc),
        };
      }
    }
    return null;
  }

  // ── Static ───────────────────────────────────────────────

  /**
   * Create a detector from OpenAI-style messages.
   * Extracts tool_calls from assistant messages.
   *
   * @param {Array<{role: string, tool_calls?: Array<{function: {name: string, arguments: string}}>}>>} messages
   * @param {Object} [opts]
   * @returns {DoomLoopDetector}
   */
  static fromMessages(messages, opts = {}) {
    const detector = new DoomLoopDetector(opts);
    const recent = messages.slice(-(opts.lookback || DEFAULT_LOOKBACK));

    for (const msg of recent) {
      if (msg.role !== "assistant" || !msg.tool_calls) continue;
      for (const tc of msg.tool_calls) {
        if (!tc.function?.name) continue;
        detector.record(tc.function.name, tc.function.arguments || "");
      }
    }

    return detector;
  }
}

// ── Corrective prompt ────────────────────────────────────────

/**
 * Build a corrective prompt to inject when a doom loop is detected.
 * @param {string} offender - Tool name or pattern description
 * @returns {string}
 */
export function buildCorrectivePrompt(offender) {
  return (
    `⚠ Doom loop detected on '${offender}'. Change approach: either use a ` +
    `DIFFERENT tool/action, or if you must use '${offender}', call it with meaningfully ` +
    `different arguments. Otherwise declare noop or escalate to the operator.`
  );
}

export default DoomLoopDetector;
