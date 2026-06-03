/**
 * signal-action-map.test.mjs — Tests for signal-action map.
 *
 * Run: node scripts/fleet-executors/signal-action-map.test.mjs
 */

import {
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
} from "./signal-action-map.mjs";

let passed = 0;
let failed = 0;

function assert(condition, label) {
  if (condition) {
    passed++;
    console.log(`  ✓ ${label}`);
  } else {
    failed++;
    console.error(`  ✗ ${label}`);
  }
}

// ── ActionRegistry ───────────────────────────────────────────

console.log("ActionRegistry:");
{
  // Built-in actions are registered
  assert(ActionRegistry.get("reply") !== undefined, "reply is registered");
  assert(ActionRegistry.get("ignore") !== undefined, "ignore is registered");
  assert(ActionRegistry.get("create_issue") !== undefined, "create_issue is registered");
  assert(ActionRegistry.get("create_pr") !== undefined, "create_pr is registered");
  assert(ActionRegistry.get("run_command") !== undefined, "run_command is registered");

  // Has metadata
  const reply = ActionRegistry.get("reply");
  assert(reply.description.includes("reply"), "reply has description");
  assert(reply.params.includes("content"), "reply has params");
  assert(reply.category === "messaging", "reply is in messaging category");

  // Category browsing
  const messaging = ActionRegistry.byCategory("messaging");
  assert(messaging.includes("reply"), "messaging contains reply");
  assert(messaging.includes("send_dm"), "messaging contains send_dm");

  const git = ActionRegistry.byCategory("git");
  assert(git.includes("create_pr"), "git contains create_pr");
  assert(git.includes("merge_pr"), "git contains merge_pr");

  // Custom registration
  ActionRegistry.register("custom_action", {
    description: "A custom test action",
    params: "foo (string)",
    category: "testing",
  });
  assert(ActionRegistry.get("custom_action") !== undefined, "custom action registered");
  assert(ActionRegistry.byCategory("testing").includes("custom_action"), "custom action in category");

  // Categories summary
  const cats = ActionRegistry.categories();
  assert(cats.messaging > 0, "messaging category has actions");
  assert(cats.git > 0, "git category has actions");
}

// ── CORE_ACTIONS ─────────────────────────────────────────────

console.log("\nCORE_ACTIONS:");
{
  assert(CORE_ACTIONS.includes("ignore"), "core includes ignore");
  assert(CORE_ACTIONS.includes("reply"), "core includes reply");
  assert(CORE_ACTIONS.includes("read_file"), "core includes read_file");
  assert(CORE_ACTIONS.includes("run_command"), "core includes run_command");
  assert(CORE_ACTIONS.includes("search_knowledge"), "core includes search_knowledge");
  assert(!CORE_ACTIONS.includes("merge_pr"), "core does NOT include merge_pr");
  assert(!CORE_ACTIONS.includes("deploy_service"), "core does NOT include deploy_service");
}

// ── SIGNAL_CONTEXT_ACTIONS ───────────────────────────────────

console.log("\nSIGNAL_CONTEXT_ACTIONS:");
{
  // DM gets no extra actions (just core)
  assert(SIGNAL_CONTEXT_ACTIONS.dm_received.length === 0, "dm_received has no extras");

  // Issue opened gets assignment/label/close
  const issue = SIGNAL_CONTEXT_ACTIONS.issue_opened;
  assert(issue.includes("assign_issue"), "issue_opened includes assign_issue");
  assert(issue.includes("label_issue"), "issue_opened includes label_issue");
  assert(issue.includes("close_issue"), "issue_opened includes close_issue");

  // PR opened gets review/merge
  const pr = SIGNAL_CONTEXT_ACTIONS.pr_opened;
  assert(pr.includes("review_pr"), "pr_opened includes review_pr");
  assert(pr.includes("merge_pr"), "pr_opened includes merge_pr");

  // Every signal type defined
  assert(typeof SIGNAL_CONTEXT_ACTIONS === "object", "SIGNAL_CONTEXT_ACTIONS is defined");
  assert(Object.keys(SIGNAL_CONTEXT_ACTIONS).length > 10, "has 10+ signal types");
}

// ── getActionsForSignal ──────────────────────────────────────

console.log("\ngetActionsForSignal:");
{
  // DM: core only
  const dmActions = getActionsForSignal("dm_received");
  assert(dmActions.includes("reply"), "dm includes reply");
  assert(dmActions.includes("ignore"), "dm includes ignore");
  assert(!dmActions.includes("merge_pr"), "dm does NOT include merge_pr");

  // Issue: core + contextual
  const issueActions = getActionsForSignal("issue_opened");
  assert(issueActions.includes("reply"), "issue includes reply (core)");
  assert(issueActions.includes("assign_issue"), "issue includes assign_issue (contextual)");
  assert(issueActions.includes("label_issue"), "issue includes label_issue (contextual)");

  // PR: core + contextual
  const prActions = getActionsForSignal("pr_opened");
  assert(prActions.includes("review_pr"), "pr includes review_pr");
  assert(prActions.includes("merge_pr"), "pr includes merge_pr");
  assert(prActions.includes("read_file"), "pr includes read_file (core)");

  // Core-only mode
  const coreOnly = getActionsForSignal("pr_opened", { coreOnly: true });
  assert(!coreOnly.includes("review_pr"), "core-only excludes review_pr");
  assert(coreOnly.includes("reply"), "core-only includes reply");

  // Unknown signal: core only
  const unknown = getActionsForSignal("totally_unknown_signal");
  assert(unknown.includes("reply"), "unknown signal still has core actions");

  // With extra categories
  const withDeploy = getActionsForSignal("dm_received", { extraCategories: ["deployment"] });
  // (depends on custom registrations from earlier test)
}

// ── getSelectionMode ─────────────────────────────────────────

console.log("\ngetSelectionMode:");
{
  assert(getSelectionMode("dm_received") === "aggressive", "dm is aggressive");
  assert(getSelectionMode("channel_mention") === "aggressive", "mention is aggressive");
  assert(getSelectionMode("channel_message") === "moderate", "channel is moderate");
  assert(getSelectionMode("scheduled_tick") === "lenient", "tick is lenient");
  assert(getSelectionMode("unknown_signal") === "moderate", "unknown defaults to moderate");
}

// ── isTaskBearing ────────────────────────────────────────────

console.log("\nisTaskBearing:");
{
  assert(isTaskBearing("issue_opened"), "issue_opened is task-bearing");
  assert(isTaskBearing("pr_opened"), "pr_opened is task-bearing");
  assert(isTaskBearing("bounty_created"), "bounty_created is task-bearing");
  assert(isTaskBearing("swarm_subtask_available"), "swarm_subtask_available is task-bearing");
  assert(isTaskBearing("scheduled_tick"), "scheduled_tick is task-bearing");
  assert(!isTaskBearing("dm_received"), "dm_received is NOT task-bearing");
  assert(!isTaskBearing("channel_message"), "channel_message is NOT task-bearing");
}

// ── isTerminal ───────────────────────────────────────────────

console.log("\nisTerminal:");
{
  assert(isTerminal("ignore"), "ignore is terminal");
  assert(isTerminal("reply"), "reply is terminal");
  assert(isTerminal("send_dm"), "send_dm is terminal");
  assert(isTerminal("merge_pr"), "merge_pr is terminal");
  assert(!isTerminal("read_file"), "read_file is NOT terminal");
  assert(!isTerminal("run_command"), "run_command is NOT terminal");
  assert(!isTerminal("web_search"), "web_search is NOT terminal");
}

// ── formatActionsForPrompt ───────────────────────────────────

console.log("\nformatActionsForPrompt:");
{
  const formatted = formatActionsForPrompt(["reply", "ignore", "create_issue"]);
  assert(formatted.includes("- reply:"), "has reply entry");
  assert(formatted.includes("- ignore:"), "has ignore entry");
  assert(formatted.includes("- create_issue:"), "has create_issue entry");
  assert(formatted.includes("content"), "mentions params");

  // Unknown action
  const withUnknown = formatActionsForPrompt(["reply", "nonexistent_action"]);
  assert(withUnknown.includes("- nonexistent_action"), "includes unknown action");
}

// ── buildActionPromptSection ─────────────────────────────────

console.log("\nbuildActionPromptSection:");
{
  const section = buildActionPromptSection("issue_opened");
  assert(section.includes("Available Actions"), "has header");
  assert(section.includes("issue_opened"), "mentions signal type");
  assert(section.includes("assign_issue"), "includes contextual action");
  assert(section.includes("actionable work"), "task-bearing signal gets note");

  // Non-task-bearing signal
  const dmSection = buildActionPromptSection("dm_received");
  assert(!dmSection.includes("actionable work"), "non-task-bearing has no note");

  // Core-only mode
  const coreSection = buildActionPromptSection("pr_opened", { coreOnly: true });
  assert(!coreSection.includes("review_pr"), "core-only excludes contextual");
}

// ── Integration with GoalLoop ────────────────────────────────

console.log("\nIntegration (action sets are composable):");
{
  // Simulate what GoalLoop would do
  const signal = "pr_opened";
  const actions = getActionsForSignal(signal);
  const formatted = formatActionsForPrompt(actions);

  assert(formatted.length > 100, "formatted actions are substantial");
  assert(actions.length > CORE_ACTIONS.length, "signal actions > core actions");

  // Progressive disclosure reduces token count
  const coreOnly = getActionsForSignal(signal, { coreOnly: true });
  const coreFormatted = formatActionsForPrompt(coreOnly);
  assert(coreFormatted.length < formatted.length, "core-only is shorter");
}

// ── Results ──────────────────────────────────────────────────

console.log(`\n${passed} passed, ${failed} failed`);
if (failed > 0) throw new Error(`${failed} test(s) failed`);
