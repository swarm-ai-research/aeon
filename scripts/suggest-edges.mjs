#!/usr/bin/env node
/**
 * suggest-edges — densify the note graph by proposing wikilinks for
 * high-similarity pairs that are not yet hard-linked.
 *
 * Pipeline:
 *   1. Load notegraph.json (regenerate first if stale or absent).
 *   2. For every pair with similarity ≥ MIN_SCORE that has no hard edge in
 *      either direction, score by (similarity × shared-term confidence).
 *   3. Filter against memory/state/suggest-edges.json so accepted or already-
 *      proposed pairs are not re-suggested.
 *   4. Filter source notes that are already well-connected (≥ MAX_OUT outgoing
 *      hard edges) — densify the thin parts of the graph, not the hubs.
 *   5. Take top N proposals and append a "## Related notes" section to each
 *      source note containing the matching wikilinks. Each pair lands as one
 *      edit on one file.
 *
 * Usage:
 *   node scripts/suggest-edges.mjs           # apply top-N edits and write state
 *   node scripts/suggest-edges.mjs --dry-run # print proposals, no writes
 *   node scripts/suggest-edges.mjs --json    # machine-readable proposal list
 *
 * Tuning constants are at the top of the file. The defaults are conservative:
 * 3 proposals/run, similarity ≥ 0.40, source already has < 5 outgoing edges.
 */
import { readFileSync, writeFileSync, existsSync, mkdirSync } from "node:fs";
import { resolve, relative, basename, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { execFileSync } from "node:child_process";

const ROOT = resolve(fileURLToPath(new URL("..", import.meta.url)));
const NOTEGRAPH_PATH = resolve(ROOT, "notegraph.json");
const STATE_PATH = resolve(ROOT, "memory/state/suggest-edges.json");

// ── tuning ─────────────────────────────────────────────────────────────────
const MIN_SCORE = 0.40;     // similarity threshold for "obviously should link"
const MAX_OUT = 5;          // skip sources with this many outgoing hard edges already
const MAX_SUGGESTIONS = 3;  // proposals per run

// ── helpers ────────────────────────────────────────────────────────────────
function parseArgv(argv) {
  const opts = { dryRun: false, json: false };
  for (const a of argv) {
    if (a === "--dry-run") opts.dryRun = true;
    else if (a === "--json") opts.json = true;
    else if (a === "-h" || a === "--help") opts.help = true;
  }
  return opts;
}

function loadJson(path, fallback) {
  if (!existsSync(path)) return fallback;
  return JSON.parse(readFileSync(path, "utf8"));
}

function loadState() {
  return loadJson(STATE_PATH, { applied: [], rejected: [], lastRun: null });
}

function saveState(state) {
  mkdirSync(dirname(STATE_PATH), { recursive: true });
  writeFileSync(STATE_PATH, JSON.stringify(state, null, 2));
}

function ensureFreshNotegraph() {
  // If notegraph.json is older than any tracked .md, regenerate. Cheap to
  // call (the extractor is fast and silent on no-change semantically).
  if (!existsSync(NOTEGRAPH_PATH)) {
    execFileSync("node", ["scripts/notegraph.mjs"], { cwd: ROOT, stdio: "inherit" });
    return;
  }
  // We don't check timestamps here — the daily notegraph skill runs at 05:00
  // and this skill runs after it. If a corpus edit landed mid-day, the next
  // notegraph tick picks it up. Re-running the extractor every time would
  // duplicate work for no gain.
}

function pairKey(a, b) { return a < b ? `${a}|${b}` : `${b}|${a}`; }

// ── core: find proposals ───────────────────────────────────────────────────
function findProposals(graph, state) {
  // Build hard-edge sets (both directions).
  const hardEdges = new Set();
  const outDeg = new Map();
  for (const n of graph.nodes) outDeg.set(n.id, 0);
  for (const e of graph.edges) {
    if (e.hardness !== "hard") continue;
    hardEdges.add(pairKey(e.source, e.target));
    outDeg.set(e.source, (outDeg.get(e.source) || 0) + 1);
  }

  // Stateful exclusions: a pair we already applied, or rejected, must not
  // re-appear. We key on the unordered pair so the direction doesn't matter.
  const excluded = new Set([
    ...state.applied.map((a) => pairKey(a.source, a.target)),
    ...state.rejected.map((r) => pairKey(r.source, r.target)),
  ]);

  // Walk similarity edges, dedupe to unordered pairs, score.
  const seenPair = new Set();
  const proposals = [];
  for (const e of graph.edges) {
    if (e.type !== "similar") continue;
    if (e.weight < MIN_SCORE) continue;
    const key = pairKey(e.source, e.target);
    if (seenPair.has(key)) continue;
    seenPair.add(key);
    if (hardEdges.has(key)) continue;   // already linked
    if (excluded.has(key)) continue;     // already handled in prior runs

    // Choose source direction: append the wikilink to whichever note has
    // *fewer* outgoing hard edges, so we densify the thin side. If tied,
    // pick alphabetically for determinism.
    const a = e.source, b = e.target;
    const [source, target] = (outDeg.get(a) || 0) <= (outDeg.get(b) || 0)
      ? (outDeg.get(a) === outDeg.get(b) && a > b ? [b, a] : [a, b])
      : [b, a];

    if ((outDeg.get(source) || 0) >= MAX_OUT) continue;
    proposals.push({
      source,
      target,
      score: e.weight,
      shared: e.shared || [],
    });
  }

  // Rank by similarity, take the top.
  proposals.sort((a, b) => b.score - a.score);
  return proposals.slice(0, MAX_SUGGESTIONS);
}

// ── editing: append "## Related notes" with wikilinks ──────────────────────
const RELATED_HEADING = "## Related notes";
const RELATED_FOOTER = "<!-- suggested by scripts/suggest-edges.mjs — edit or remove freely -->";

function buildBasenameIndex(noteIds) {
  // Lowercased basename (without .md) → count. notegraph's resolver matches
  // wikilinks by basename only when there's exactly one — anything ambiguous
  // silently fails to resolve, so we need to detect and disambiguate here.
  const counts = new Map();
  for (const id of noteIds) {
    const b = basename(id, ".md").toLowerCase();
    counts.set(b, (counts.get(b) || 0) + 1);
  }
  return counts;
}

function wikilinkFor(targetPath, basenameCounts) {
  // If the basename is unique across the corpus, the short [[basename]] form
  // resolves cleanly via notegraph's basename lookup. If it's ambiguous (e.g.
  // memory.md vs MEMORY.md, index.md vs INDEX.md), emit the full repo-root
  // path with .md — notegraph's resolver handles that via exact-id match.
  const b = basename(targetPath, ".md");
  const isAmbiguous = (basenameCounts.get(b.toLowerCase()) || 0) > 1;
  return isAmbiguous ? `[[${targetPath}]]` : `[[${b}]]`;
}

function applyProposal(proposal, byId, basenameCounts) {
  const sourcePath = resolve(ROOT, proposal.source);
  const target = byId.get(proposal.target);
  if (!target) throw new Error(`unknown target: ${proposal.target}`);
  const existing = readFileSync(sourcePath, "utf8");
  const link = wikilinkFor(proposal.target, basenameCounts);
  const bullet = `- ${link} — ${target.title.replace(/\n/g, " ")} _(similarity ${proposal.score.toFixed(2)})_`;

  let out;
  // If the note already has a "## Related notes" block, append into it.
  // Otherwise create one at the end. The footer comment lets future runs
  // identify the block reliably.
  const headingIdx = existing.indexOf(RELATED_HEADING);
  if (headingIdx >= 0) {
    // Insert the new bullet at the end of the block — before the footer if
    // present, otherwise before the next heading or EOF.
    const footerIdx = existing.indexOf(RELATED_FOOTER, headingIdx);
    let insertAt;
    if (footerIdx >= 0) {
      insertAt = footerIdx;
    } else {
      // find next H1/H2 after the heading, or EOF
      const after = existing.slice(headingIdx + RELATED_HEADING.length);
      const nextH = after.search(/\n#{1,2} /);
      insertAt = nextH >= 0 ? headingIdx + RELATED_HEADING.length + nextH : existing.length;
    }
    out = existing.slice(0, insertAt).replace(/\s*$/, "") + `\n${bullet}\n\n` + existing.slice(insertAt);
  } else {
    const trimmed = existing.replace(/\s+$/, "");
    out = `${trimmed}\n\n${RELATED_HEADING}\n\n${bullet}\n\n${RELATED_FOOTER}\n`;
  }
  writeFileSync(sourcePath, out);
  return { path: proposal.source, bullet };
}

// ── main ───────────────────────────────────────────────────────────────────
function main() {
  const opts = parseArgv(process.argv.slice(2));
  if (opts.help) {
    process.stdout.write(
      `Usage: node scripts/suggest-edges.mjs [--dry-run] [--json]\n` +
      `\n` +
      `Reads notegraph.json, picks ${MAX_SUGGESTIONS} highest-similarity unlinked pairs\n` +
      `(score ≥ ${MIN_SCORE}, source out-degree < ${MAX_OUT}), and appends a\n` +
      `"## Related notes" wikilink to the source of each. Tracks proposed pairs\n` +
      `in memory/state/suggest-edges.json to avoid re-suggesting.\n`,
    );
    return;
  }

  ensureFreshNotegraph();
  const graph = loadJson(NOTEGRAPH_PATH, null);
  if (!graph) { process.stderr.write("notegraph.json not found and could not be generated\n"); process.exit(1); }
  const state = loadState();
  const byId = new Map(graph.nodes.map((n) => [n.id, n]));
  const basenameCounts = buildBasenameIndex(graph.nodes.map((n) => n.id));

  const proposals = findProposals(graph, state);

  if (opts.json) {
    process.stdout.write(JSON.stringify({ proposals, applied: !opts.dryRun }, null, 2));
    return;
  }

  if (proposals.length === 0) {
    process.stdout.write("suggest-edges: no new high-similarity unlinked pairs above threshold\n");
    return;
  }

  process.stdout.write(`suggest-edges: ${proposals.length} proposal(s) (similarity ≥ ${MIN_SCORE})\n`);
  for (const p of proposals) {
    const src = byId.get(p.source);
    const tgt = byId.get(p.target);
    process.stdout.write(
      `  ${p.score.toFixed(3)}  ${src.title} → ${tgt.title}\n` +
      `    source: ${p.source}\n` +
      `    target: ${p.target}\n` +
      `    shared: [${p.shared.join(", ")}]\n`,
    );
  }

  if (opts.dryRun) {
    process.stdout.write("\n(--dry-run: no files modified, state not updated)\n");
    return;
  }

  const applied = [];
  for (const p of proposals) {
    const { path, bullet } = applyProposal(p, byId, basenameCounts);
    applied.push({ source: p.source, target: p.target, score: p.score, shared: p.shared, bullet, appliedAt: new Date().toISOString() });
    process.stdout.write(`  wrote ${path}\n`);
  }

  state.applied = [...state.applied, ...applied];
  state.lastRun = new Date().toISOString();
  saveState(state);
  process.stdout.write(`\n  state: ${relative(ROOT, STATE_PATH)} (${state.applied.length} total applied)\n`);
}

main();
