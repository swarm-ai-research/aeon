/**
 * wake-up-stack.mjs — Tiered context assembly for agent knowledge retrieval.
 *
 * Ported from Nookplot's wake_up_stack.py. Replaces flat single-shot RAG
 * with a 4-layer stack that balances cost and coverage:
 *
 *   L0 (Identity, ~50 tok)    — Always loaded. Agent's role + top domains.
 *   L1 (Essentials, ~300 tok) — Session-cached. Top syntheses + recent items.
 *   L2 (On-Demand, ~400 tok) — Per-signal when task diverges from L1 coverage.
 *   L3 (Deep Search)          — Explicit tool call only. Not part of this module.
 *
 * The key insight: most signals stay within the agent's domain (L1 suffices).
 * L2 fires only when the task description has low keyword overlap with L1
 * content — a cheap divergence check before paying for semantic search.
 *
 * Query segmentation (included) breaks tasks into multiple sub-queries to
 * solve the "center of mass" problem in standard RAG: a single pooled query
 * embedding averages away individual concepts. Multi-granularity queries
 * with MAX similarity matching recover those signals.
 *
 * Usage:
 *   import { WakeUpStack, segmentQuery } from "./wake-up-stack.mjs";
 *
 *   const stack = new WakeUpStack({
 *     identity: { role: "code reviewer", domains: ["security", "performance"] },
 *     retrieveEssentials: async () => [{ text: "...", score: 0.9 }],
 *     retrieveOnDemand: async (query) => [{ text: "...", score: 0.8 }],
 *   });
 *
 *   const context = await stack.getContext("review this PR for security issues");
 *   // → { l0: "...", l1: [...], l2: [...], markdown: "combined context" }
 */

// ── Constants ────────────────────────────────────────────────

/** L1 cache TTL in milliseconds */
const L1_TTL_MS = 30 * 60 * 1000; // 30 minutes

/** Minimum keyword overlap ratio to skip L2 search */
const L2_OVERLAP_THRESHOLD = 0.2;

/** Max items in L1 cache */
const L1_MAX_ITEMS = 20;

/** Max items returned from L2 */
const L2_MAX_ITEMS = 10;

// ── Query Segmentation ───────────────────────────────────────

/**
 * @typedef {Object} SegmentedQuery
 * @property {string} full — Complete task string
 * @property {string[]} segments — Sliding-window substrings
 * @property {string[]} entities — Extracted entities (#hashtags, @mentions, Capitalized Phrases)
 * @property {string[]} questions — Noun phrases from question anchors
 */

const HASHTAG_RE = /[#@]\w+/g;
const CAP_PHRASE_RE = /\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+/g;
const QUESTION_RE = /(?:what is|how do i|how to|why does|when should)\s+([a-z\s]{3,40})/gi;

/**
 * Decompose a task description into multiple query granularities.
 *
 * Solves the "center of mass" problem: a single pooled query embedding
 * averages away individual concepts. By splitting into full + segments +
 * entities + questions, we let semantic search take MAX similarity across
 * all of them.
 *
 * @param {string} task - Task description
 * @param {number} [maxSegments=3] - Max sliding-window segments
 * @returns {SegmentedQuery}
 */
export function segmentQuery(task, maxSegments = 3) {
  if (typeof task !== "string") {
    return { full: "", segments: [], entities: [], questions: [] };
  }

  const full = task.trim();

  // Sliding window segments (only for longer tasks)
  const segments = [];
  if (full.length > 60) {
    const words = full.split(/\s+/);
    const segmentSize = Math.ceil(words.length / maxSegments);
    const overlap = Math.max(1, Math.floor(segmentSize * 0.3));

    for (let i = 0; i < words.length && segments.length < maxSegments; i += segmentSize - overlap) {
      const segment = words.slice(i, i + segmentSize).join(" ");
      if (segment.length > 20) {
        segments.push(segment);
      }
    }
  }

  // Entity extraction
  const entities = [];
  for (const match of full.matchAll(HASHTAG_RE)) {
    entities.push(match[0]);
  }
  for (const match of full.matchAll(CAP_PHRASE_RE)) {
    if (!entities.includes(match[0])) {
      entities.push(match[0]);
    }
  }

  // Question anchor extraction
  const questions = [];
  for (const match of full.matchAll(QUESTION_RE)) {
    const phrase = match[1].trim();
    if (phrase.length > 2 && !questions.includes(phrase)) {
      questions.push(phrase);
    }
  }

  return { full, segments, entities, questions };
}

// ── Keyword Overlap ──────────────────────────────────────────

/**
 * Extract keywords from text (lowercase, deduplicated, stopwords removed).
 * @param {string} text
 * @returns {Set<string>}
 */
function extractKeywords(text) {
  if (typeof text !== "string") return new Set();

  const STOPWORDS = new Set([
    "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did", "will", "would", "could",
    "should", "may", "might", "shall", "can", "to", "of", "in", "for",
    "on", "with", "at", "by", "from", "as", "into", "through", "during",
    "before", "after", "above", "below", "between", "and", "but", "or",
    "not", "no", "nor", "so", "yet", "both", "either", "neither", "each",
    "every", "all", "any", "few", "more", "most", "other", "some", "such",
    "than", "too", "very", "just", "about", "up", "out", "it", "its",
    "this", "that", "these", "those", "i", "me", "my", "we", "our",
    "you", "your", "he", "him", "his", "she", "her", "they", "them",
    "their", "what", "which", "who", "whom", "when", "where", "why", "how",
  ]);

  return new Set(
    text.toLowerCase()
      .replace(/[^a-z0-9\s]/g, " ")
      .split(/\s+/)
      .filter(w => w.length > 2 && !STOPWORDS.has(w))
  );
}

/**
 * Calculate keyword overlap ratio between two texts.
 * Returns 0-1: fraction of task keywords found in context keywords.
 *
 * @param {string} taskText
 * @param {string} contextText
 * @returns {number}
 */
export function keywordOverlap(taskText, contextText) {
  const taskKw = extractKeywords(taskText);
  const contextKw = extractKeywords(contextText);

  if (taskKw.size === 0) return 0;

  let overlap = 0;
  for (const kw of taskKw) {
    if (contextKw.has(kw)) overlap++;
  }

  return overlap / taskKw.size;
}

/**
 * Calculate overlap between task keywords and a list of context items.
 *
 * @param {string} taskText
 * @param {Array<{text: string}>} items
 * @returns {number} Max overlap ratio across all items
 */
function maxItemOverlap(taskText, items) {
  if (!items || items.length === 0) return 0;
  let max = 0;
  for (const item of items) {
    const overlap = keywordOverlap(taskText, item.text || "");
    if (overlap > max) max = overlap;
  }
  return max;
}

// ── WakeUpStack ──────────────────────────────────────────────

/**
 * @typedef {Object} KnowledgeItem
 * @property {string} text — The knowledge content
 * @property {number} [score] — Relevance score (0-1)
 * @property {string} [source] — Where this came from
 * @property {string} [id] — Unique identifier for caching
 */

/**
 * @typedef {Object} WakeUpStackOptions
 * @property {{ role: string, domains: string[] }} identity — Agent identity (L0)
 * @property {Function} [retrieveEssentials] — async () => KnowledgeItem[] — L1 provider
 * @property {Function} [retrieveOnDemand] — async (query: string, mode: string) => KnowledgeItem[] — L2 provider
 * @property {number} [l1TtlMs] — L1 cache TTL (default 30 min)
 * @property {number} [overlapThreshold] — L2 trigger threshold (default 0.2)
 * @property {boolean} [verbose] — Log decisions
 */

export class WakeUpStack {
  /**
   * @param {WakeUpStackOptions} options
   */
  constructor(options) {
    this._identity = options.identity || { role: "agent", domains: [] };
    this._retrieveEssentials = options.retrieveEssentials || (async () => []);
    this._retrieveOnDemand = options.retrieveOnDemand || (async () => []);
    this._l1TtlMs = options.l1TtlMs || L1_TTL_MS;
    this._overlapThreshold = options.overlapThreshold || L2_OVERLAP_THRESHOLD;
    this._verbose = options.verbose || false;

    // L1 cache
    this._l1Cache = null;
    this._l1CacheTime = 0;
  }

  /**
   * Build context for a signal/task.
   *
   * Assembles L0 (always) + L1 (cached) + L2 (if divergence detected).
   *
   * @param {string} taskDescription — What the agent is about to do
   * @param {string} [signalType] — Signal type (for selection mode)
   * @returns {Promise<{ l0: string, l1: KnowledgeItem[], l2: KnowledgeItem[], markdown: string }>}
   */
  async getContext(taskDescription = "", signalType = null) {
    // ── L0: Identity (always loaded) ─────────────────────────
    const l0 = this._buildL0();

    // ── L1: Essentials (session-cached) ──────────────────────
    const l1 = await this._getL1();

    // ── L2: On-demand (divergence-triggered) ─────────────────
    const l2 = await this._getL2(taskDescription, signalType, l1);

    // ── Assemble markdown ────────────────────────────────────
    const markdown = this._assembleMarkdown(l0, l1, l2);

    return { l0, l1, l2, markdown };
  }

  /**
   * Invalidate the L1 cache (call when knowledge changes).
   */
  invalidateL1() {
    this._l1Cache = null;
    this._l1CacheTime = 0;
  }

  // ── Private ────────────────────────────────────────────────

  /** @private */
  _buildL0() {
    const { role, domains } = this._identity;
    const domainStr = domains.length > 0 ? domains.join(", ") : "general";
    return `Role: ${role}\nDomains: ${domainStr}`;
  }

  /** @private */
  async _getL1() {
    const now = Date.now();
    if (this._l1Cache && (now - this._l1CacheTime) < this._l1TtlMs) {
      return this._l1Cache;
    }

    try {
      const items = await this._retrieveEssentials();
      this._l1Cache = (items || []).slice(0, L1_MAX_ITEMS);
      this._l1CacheTime = now;
    } catch (err) {
      if (this._verbose) console.warn("[wake-up-stack] L1 fetch failed:", err.message);
      this._l1Cache = this._l1Cache || [];
    }

    return this._l1Cache;
  }

  /** @private */
  async _getL2(taskDescription, signalType, l1Items) {
    if (!taskDescription || typeof taskDescription !== "string") return [];

    // Check overlap with L1 — skip L2 if task is within L1 coverage
    const overlap = maxItemOverlap(taskDescription, l1Items);
    if (overlap >= this._overlapThreshold) {
      if (this._verbose) {
        console.log(`[wake-up-stack] L2 skipped — overlap ${(overlap * 100).toFixed(0)}% >= ${(this._overlapThreshold * 100).toFixed(0)}%`);
      }
      return [];
    }

    // Segment the query for multi-granularity retrieval
    const segmented = segmentQuery(taskDescription);

    // Build the search query — combine full + entities + questions
    const queryParts = [segmented.full];
    if (segmented.entities.length > 0) {
      queryParts.push(...segmented.entities);
    }
    if (segmented.questions.length > 0) {
      queryParts.push(...segmented.questions);
    }

    const searchQuery = queryParts.join(" ");

    try {
      const items = await this._retrieveOnDemand(searchQuery, signalType || "moderate");
      return (items || []).slice(0, L2_MAX_ITEMS);
    } catch (err) {
      if (this._verbose) console.warn("[wake-up-stack] L2 fetch failed:", err.message);
      return [];
    }
  }

  /** @private */
  _assembleMarkdown(l0, l1, l2) {
    const sections = [];

    // L0
    sections.push("## Identity\n" + l0);

    // L1
    if (l1.length > 0) {
      const l1Text = l1.map(item => `- ${item.text}`).join("\n");
      sections.push("## Essentials\n" + l1Text);
    }

    // L2
    if (l2.length > 0) {
      const l2Text = l2.map(item => `- ${item.text}`).join("\n");
      sections.push("## Context\n" + l2Text);
    }

    return sections.join("\n\n");
  }
}

export default { WakeUpStack, segmentQuery, keywordOverlap };
