#!/usr/bin/env node
// Compute deltas between the freshly-written notegraph.json and HEAD's copy.
// Emits a JSON summary on stdout that the SKILL step 3/4 driver can consume.

import { execSync } from 'node:child_process';
import { readFileSync } from 'node:fs';

const current = JSON.parse(readFileSync('notegraph.json', 'utf8'));

let previous;
try {
  const raw = execSync('git show HEAD:notegraph.json', { encoding: 'utf8' });
  previous = JSON.parse(raw);
} catch {
  previous = null;
}

const cs = current.stats;
const ps = previous?.stats ?? { nodes: 0, edges: 0, hard: 0, soft: 0, orphans: 0, atomic: 0, bundled: 0 };

const nodeOf = (g) => new Map((g?.nodes ?? []).map((n) => [n.id, n]));
const prevNodes = nodeOf(previous);
const curNodes = nodeOf(current);

const isOrphan = (n) => n && (n.inDegree ?? 0) === 0 && (n.outDegree ?? 0) === 0;

const currentOrphans = [...curNodes.values()].filter(isOrphan).map((n) => n.id);
const previousOrphans = new Set([...prevNodes.values()].filter(isOrphan).map((n) => n.id));

const new_orphans = currentOrphans.filter((id) => !previousOrphans.has(id));
const resolved_orphans = [...previousOrphans].filter((id) => !curNodes.has(id) || !isOrphan(curNodes.get(id)));

const currentBundled = [...curNodes.values()].filter((n) => n.bundled === true).map((n) => n.id);
const previousBundled = new Set([...prevNodes.values()].filter((n) => n.bundled === true).map((n) => n.id));

const new_bundled = currentBundled.filter((id) => !previousBundled.has(id));
const resolved_bundled = [...previousBundled].filter((id) => !curNodes.has(id) || curNodes.get(id).bundled !== true);

const new_nodes = [...curNodes.keys()].filter((id) => !prevNodes.has(id));
const removed_nodes = [...prevNodes.keys()].filter((id) => !curNodes.has(id));

const node_delta = cs.nodes - ps.nodes;
const edge_delta = cs.edges - ps.edges;
const orphan_delta = cs.orphans - ps.orphans;
const bundled_delta = (cs.bundled ?? 0) - (ps.bundled ?? 0);
const hard_delta = cs.hard - ps.hard;
const soft_delta = cs.soft - ps.soft;
const atomic_delta = (cs.atomic ?? 0) - (ps.atomic ?? 0);

let verdict;
if (new_bundled.length > 0) {
  verdict = `${new_bundled.length} new bundled note(s): ${new_bundled[0]}${new_bundled.length > 1 ? '…' : ''}`;
} else if (new_orphans.length > 0) {
  verdict = `${new_orphans.length} new orphan(s): ${new_orphans[0]}${new_orphans.length > 1 ? '…' : ''}`;
} else if (node_delta > 0 && orphan_delta <= 0 && bundled_delta <= 0) {
  verdict = `+${node_delta} notes wired in`;
} else if (edge_delta > 10) {
  verdict = `+${edge_delta} new edges`;
} else {
  verdict = `graph refreshed (${cs.nodes}n / ${cs.edges}e / ${cs.bundled ?? 0}b)`;
}

const diffQuiet = (() => {
  try {
    execSync('git diff --quiet notegraph.json docs/notegraph.md docs/notegraph.html', { stdio: 'ignore' });
    return true;
  } catch {
    return false;
  }
})();

const summary = {
  verdict_one_line: verdict,
  diff_quiet: diffQuiet,
  current_stats: cs,
  previous_stats: ps,
  delta: {
    nodes: node_delta,
    edges: edge_delta,
    hard: hard_delta,
    soft: soft_delta,
    orphans: orphan_delta,
    bundled: bundled_delta,
    atomic: atomic_delta,
  },
  new_orphans,
  resolved_orphans,
  new_bundled,
  resolved_bundled,
  new_nodes,
  removed_nodes,
  current_orphans: currentOrphans,
};

process.stdout.write(JSON.stringify(summary, null, 2) + '\n');
