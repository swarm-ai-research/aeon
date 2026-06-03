/**
 * signal-action-map.mjs — Map trigger signals to available agent actions.
 *
 * Ported from Nookplot's signal_action_map.py + action_catalog.py.
 * Two core ideas:
 *
 *   1. Action Catalog — registry of every action with description, params, category.
 *      Actions are composable units: "reply", "create_issue", "run_search", etc.
 *
 *   2. Signal → Action Map — each signal type (dm_received, issue_opened, etc.)
 *      gets a set of contextual actions ON TOP of the core actions always available.
 *      This prevents an agent from, say, trying to merge a PR when it got a DM.
 *
 * Progressive disclosure: agents can be constrained to core-only when token-limited.
 *
 * Usage:
 *   import { ActionRegistry, getActionsForSignal, formatActionsForPrompt } from "./signal-action-map.mjs";
 *
 *   // Register custom actions
 *   ActionRegistry.register("deploy_service", {
 *     description: "Deploy a service to production",
 *     params: "serviceName (string), version (string)",
 *     category: "deployment",
 *   });
 *
 *   // Get actions for a signal
 *   const actions = getActionsForSignal("issue_opened");
 *   // → ["reply", "ignore", "create_comment", "assign_issue", ...]
 *
 *   // Format for LLM prompt
 *   const prompt = formatActionsForPrompt(actions);
 */

// ── Action Registry ──────────────────────────────────────────

/**
 * @typedef {Object} ActionInfo
 * @property {string} description - What the action does
 * @property {string} [params] - Parameter description
 * @property {string} [category] - Category for browsing
 */

/** @type {Map<string, ActionInfo>} */
const _actions = new Map();

/** Built-in action categories for discovery */
const BUILTIN_CATEGORIES = [
  "meta",       // ignore, execute, browse
  "messaging",  // reply, send_dm, post_comment
  "issues",     // create_issue, close_issue, label_issue
  "git",        // create_branch, commit, create_pr, merge_pr
  "search",     // web_search, search_knowledge, search_code
  "filesystem", // read_file, write_file, list_dir
  "execution",  // run_command, run_script
  "deploy",     // deploy, rollback
  "monitoring", // check_health, get_metrics
  "coordination", // swarm, bounty, delegation
];

export const ActionRegistry = {
  /**
   * Register an action.
   * @param {string} name - Unique action name
   * @param {ActionInfo} info - Action metadata
   */
  register(name, info) {
    _actions.set(name, {
      description: info.description || name,
      params: info.params || "",
      category: info.category || "uncategorized",
    });
  },

  /**
   * Register multiple actions at once.
   * @param {Record<string, ActionInfo>} catalog
   */
  registerAll(catalog) {
    for (const [name, info] of Object.entries(catalog)) {
      this.register(name, info);
    }
  },

  /**
   * Get action info.
   * @param {string} name
   * @returns {ActionInfo|undefined}
   */
  get(name) {
    return _actions.get(name);
  },

  /**
   * Get all registered action names.
   * @returns {string[]}
   */
  all() {
    return [..._actions.keys()];
  },

  /**
   * Get actions in a category.
   * @param {string} category
   * @returns {string[]}
   */
  byCategory(category) {
    return [..._actions.entries()]
      .filter(([, info]) => info.category === category)
      .map(([name]) => name);
  },

  /**
   * Get all categories with action counts.
   * @returns {Record<string, number>}
   */
  categories() {
    const cats = {};
    for (const [, info] of _actions) {
      cats[info.category] = (cats[info.category] || 0) + 1;
    }
    return cats;
  },

  /**
   * Clear all registrations (for testing).
   */
  _clear() {
    _actions.clear();
  },
};

// ── Built-in Actions ─────────────────────────────────────────

const BUILTIN_ACTIONS = {
  // ── Meta ──
  ignore: {
    description: "Skip this event and take no action",
    params: "none",
    category: "meta",
  },
  execute: {
    description: "Execute a general-purpose directive (freeform action)",
    params: "content (string)",
    category: "meta",
  },
  browse_tools: {
    description: "Discover available tools by category",
    params: "category (string, optional)",
    category: "meta",
  },

  // ── Messaging ──
  reply: {
    description: "Send a text reply to the current context",
    params: "content (string)",
    category: "messaging",
  },
  send_dm: {
    description: "Send a direct message to another agent or user",
    params: "content (string), recipient (string)",
    category: "messaging",
  },
  post_comment: {
    description: "Post a comment on an issue, PR, or discussion",
    params: "content (string), targetId (string)",
    category: "messaging",
  },

  // ── Issues ──
  create_issue: {
    description: "Create a new issue or task",
    params: "title (string), body (string), labels (string[], optional)",
    category: "issues",
  },
  close_issue: {
    description: "Close an existing issue",
    params: "issueId (string), reason (string, optional)",
    category: "issues",
  },
  label_issue: {
    description: "Add labels to an issue",
    params: "issueId (string), labels (string[])",
    category: "issues",
  },
  assign_issue: {
    description: "Assign an issue to someone",
    params: "issueId (string), assignee (string)",
    category: "issues",
  },

  // ── Git ──
  create_branch: {
    description: "Create a new git branch",
    params: "branchName (string), from (string, optional)",
    category: "git",
  },
  commit_files: {
    description: "Commit file changes",
    params: "files (array of {path, content}), message (string)",
    category: "git",
  },
  create_pr: {
    description: "Create a pull request",
    params: "title (string), body (string), branch (string)",
    category: "git",
  },
  merge_pr: {
    description: "Merge a pull request",
    params: "prId (string), method (string, optional)",
    category: "git",
  },
  review_pr: {
    description: "Submit a code review on a pull request",
    params: "prId (string), comments (array), verdict (string)",
    category: "git",
  },

  // ── Search ──
  web_search: {
    description: "Search the web for information",
    params: "query (string)",
    category: "search",
  },
  search_knowledge: {
    description: "Query the knowledge graph and local memory",
    params: "query (string), limit (number, optional)",
    category: "search",
  },
  search_code: {
    description: "Search codebase for patterns or files",
    params: "query (string), path (string, optional)",
    category: "search",
  },

  // ── Filesystem ──
  read_file: {
    description: "Read a file's contents",
    params: "path (string)",
    category: "filesystem",
  },
  write_file: {
    description: "Write content to a file",
    params: "path (string), content (string)",
    category: "filesystem",
  },
  list_dir: {
    description: "List files in a directory",
    params: "path (string), pattern (string, optional)",
    category: "filesystem",
  },

  // ── Execution ──
  run_command: {
    description: "Run a shell command",
    params: "command (string), cwd (string, optional)",
    category: "execution",
  },
  run_script: {
    description: "Run a script file",
    params: "path (string), args (string[], optional)",
    category: "execution",
  },

  // ── Monitoring ──
  check_health: {
    description: "Check health status of a service or endpoint",
    params: "target (string)",
    category: "monitoring",
  },
  get_metrics: {
    description: "Retrieve metrics for a service",
    params: "target (string), timeRange (string, optional)",
    category: "monitoring",
  },

  // ── Coordination ──
  claim_subtask: {
    description: "Claim an available swarm subtask",
    params: "subtaskId (string)",
    category: "coordination",
  },
  submit_result: {
    description: "Submit result for a claimed subtask or bounty",
    params: "taskId (string), content (string or object)",
    category: "coordination",
  },
  create_bounty: {
    description: "Create a bounty with a reward",
    params: "title (string), description (string), reward (number)",
    category: "coordination",
  },
  delegate_task: {
    description: "Delegate a task to another agent",
    params: "taskDescription (string), targetAgent (string)",
    category: "coordination",
  },

  // ── Deployment ──
  deploy_service: {
    description: "Deploy a service or release",
    params: "target (string), ref (string, optional)",
    category: "deploy",
  },
  rollback: {
    description: "Roll back a service to a previous known-good state",
    params: "target (string), toRef (string, optional)",
    category: "deploy",
  },
};

// Register built-in actions
ActionRegistry.registerAll(BUILTIN_ACTIONS);

// ── Core Actions (always available) ──────────────────────────

export const CORE_ACTIONS = [
  "ignore",
  "execute",
  "browse_tools",
  "reply",
  "send_dm",
  "post_comment",
  "create_issue",
  "web_search",
  "search_knowledge",
  "search_code",
  "read_file",
  "write_file",
  "run_command",
];

// ── Signal → Contextual Actions ──────────────────────────────

/**
 * Maps signal types to ADDITIONAL actions beyond core.
 * The agent always has core actions; these are contextual extras.
 *
 * Design principle: each signal type gets 0-6 extra actions that are
 * relevant to what just happened. A DM doesn't need merge_pr;
 * a PR opened event does.
 */
export const SIGNAL_CONTEXT_ACTIONS = {
  // ── Messaging signals ──
  dm_received: [],
  channel_message: [],
  channel_mention: ["create_bounty"],
  reply_to_own_post: [],

  // ── Issue signals ──
  issue_opened: ["assign_issue", "label_issue", "close_issue"],
  issue_closed: [],
  issue_assigned: ["post_comment", "close_issue"],
  issue_commented: ["close_issue", "label_issue"],
  issue_labeled: ["assign_issue"],

  // ── PR signals ──
  pr_opened: ["review_pr", "merge_pr"],
  pr_updated: ["review_pr", "merge_pr"],
  pr_closed: [],
  pr_merged: ["deploy_service"],
  review_submitted: ["merge_pr"],

  // ── Git signals ──
  push_received: ["create_pr"],
  branch_created: ["commit_files", "create_pr"],
  tag_created: ["deploy_service"],

  // ── Deployment signals ──
  deploy_started: ["check_health", "get_metrics"],
  deploy_completed: ["check_health", "get_metrics"],
  deploy_failed: ["rollback"],

  // ── Monitoring signals ──
  alert_fired: ["check_health", "get_metrics", "run_command"],
  health_check_failed: ["run_command", "check_health"],

  // ── Coordination signals ──
  bounty_created: ["claim_subtask"],
  bounty_claimed: ["submit_result"],
  swarm_subtask_available: ["claim_subtask"],
  swarm_result_submitted: [],
  task_delegated: ["submit_result"],

  // ── Cron/scheduled signals ──
  scheduled_tick: ["check_health", "get_metrics", "search_knowledge"],
  manual_trigger: [],
};

// ── Terminal Actions (end a turn) ─────────────────────────────

export const TERMINAL_ACTIONS = new Set([
  "ignore",
  "reply",
  "send_dm",
  "post_comment",
  "merge_pr",
  "close_issue",
  "submit_result",
]);

// ── Task-Bearing Signals (carry actionable work) ─────────────

export const TASK_BEARING_SIGNALS = new Set([
  "issue_opened",
  "issue_assigned",
  "issue_commented",
  "pr_opened",
  "pr_updated",
  "review_submitted",
  "bounty_created",
  "bounty_claimed",
  "swarm_subtask_available",
  "swarm_result_submitted",
  "task_delegated",
  "scheduled_tick",
  "manual_trigger",
]);

// ── Selection Modes (for knowledge retrieval integration) ────

/**
 * Signal type → retrieval focus level.
 * Used by tiered knowledge retrieval (wake-up stack) to decide
 * how aggressively to filter context.
 */
export const SIGNAL_SELECTION_MODE = {
  dm_received: "aggressive",
  channel_mention: "aggressive",
  reply_to_own_post: "aggressive",
  channel_message: "moderate",
  issue_opened: "moderate",
  issue_commented: "moderate",
  pr_opened: "moderate",
  swarm_subtask_available: "moderate",
  scheduled_tick: "lenient",
  manual_trigger: "lenient",
};

// ── Public API ────────────────────────────────────────────────

/**
 * Get all actions available for a signal type.
 *
 * @param {string} signalType - The signal that triggered the agent
 * @param {Object} [opts]
 * @param {boolean} [opts.coreOnly=false] — Progressive disclosure: return only core actions
 * @param {string[]} [opts.extraCategories] — Include all actions from these categories
 * @returns {string[]} Action names available for this signal
 */
export function getActionsForSignal(signalType, { coreOnly = false, extraCategories = [] } = {}) {
  if (coreOnly) return [...CORE_ACTIONS];

  const contextual = SIGNAL_CONTEXT_ACTIONS[signalType] || [];
  const actionSet = new Set([...CORE_ACTIONS, ...contextual]);

  // Add actions from requested categories
  for (const cat of extraCategories) {
    for (const action of ActionRegistry.byCategory(cat)) {
      actionSet.add(action);
    }
  }

  return [...actionSet];
}

/**
 * Get the selection mode for knowledge retrieval.
 *
 * @param {string} signalType
 * @returns {"aggressive"|"moderate"|"lenient"}
 */
export function getSelectionMode(signalType) {
  return SIGNAL_SELECTION_MODE[signalType] || "moderate";
}

/**
 * Check if a signal carries actionable work.
 *
 * @param {string} signalType
 * @returns {boolean}
 */
export function isTaskBearing(signalType) {
  return TASK_BEARING_SIGNALS.has(signalType);
}

/**
 * Check if an action terminates the current turn.
 *
 * @param {string} actionName
 * @returns {boolean}
 */
export function isTerminal(actionName) {
  return TERMINAL_ACTIONS.has(actionName);
}

/**
 * Format a list of action names into a descriptive string for LLM prompts.
 *
 * @param {string[]} actions - Action names to format
 * @returns {string} Formatted action descriptions
 */
export function formatActionsForPrompt(actions) {
  const lines = [];

  for (const action of actions) {
    const info = ActionRegistry.get(action);
    if (!info) {
      lines.push(`- ${action}`);
      continue;
    }
    const paramStr = info.params ? ` Params: ${info.params}` : "";
    lines.push(`- ${action}: ${info.description}.${paramStr}`);
  }

  // Add browse hint
  if (actions.includes("browse_tools")) {
    const cats = Object.keys(ActionRegistry.categories()).join(", ");
    lines.push("");
    lines.push(`Tip: Use browse_tools to discover more tools by category (${cats}).`);
  }

  return lines.join("\n");
}

/**
 * Build a system prompt section listing available actions for a signal.
 *
 * @param {string} signalType - The triggering signal
 * @param {Object} [opts] - Same as getActionsForSignal opts
 * @returns {string} Prompt section
 */
export function buildActionPromptSection(signalType, opts = {}) {
  const actions = getActionsForSignal(signalType, opts);
  const formatted = formatActionsForPrompt(actions);
  const taskBearing = isTaskBearing(signalType);

  const parts = [
    `## Available Actions (signal: ${signalType})`,
    "",
    formatted,
  ];

  if (taskBearing) {
    parts.push("", "This signal carries actionable work. Respond with one of the actions above.");
  }

  return parts.join("\n");
}

export default {
  ActionRegistry,
  CORE_ACTIONS,
  SIGNAL_CONTEXT_ACTIONS,
  TERMINAL_ACTIONS,
  TASK_BEARING_SIGNALS,
  SIGNAL_SELECTION_MODE,
  getActionsForSignal,
  getSelectionMode,
  isTaskBearing,
  isTerminal,
  formatActionsForPrompt,
  buildActionPromptSection,
};
