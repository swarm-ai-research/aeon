#!/usr/bin/env node
import { readFileSync } from 'fs';
import { execSync } from 'child_process';

const cur = JSON.parse(readFileSync('notegraph.json', 'utf8'));
let prev = null;
try {
  prev = JSON.parse(execSync('git show HEAD:notegraph.json', { encoding: 'utf8' }));
} catch (e) {
  prev = { stats: { nodes: 0, edges: 0, hard: 0, soft: 0, orphans: 0, atomic: 0, bundled: 0 }, nodes: [] };
}

const cs = cur.stats, ps = prev.stats;
const node_delta = cs.nodes - ps.nodes;
const edge_delta = cs.edges - ps.edges;
const orphan_delta = (cs.orphans || 0) - (ps.orphans || 0);
const bundled_delta = (cs.bundled || 0) - (ps.bundled || 0);

const curOrphans = new Set(cur.nodes.filter(n => n.inDegree === 0 && n.outDegree === 0).map(n => n.id));
const prevOrphans = new Set((prev.nodes || []).filter(n => n.inDegree === 0 && n.outDegree === 0).map(n => n.id));
const new_orphans = [...curOrphans].filter(id => !prevOrphans.has(id));
const resolved_orphans = [...prevOrphans].filter(id => !curOrphans.has(id));

const curBundled = new Set(cur.nodes.filter(n => n.bundled).map(n => n.id));
const prevBundled = new Set((prev.nodes || []).filter(n => n.bundled).map(n => n.id));
const new_bundled = [...curBundled].filter(id => !prevBundled.has(id));
const resolved_bundled = [...prevBundled].filter(id => !curBundled.has(id));

const curNodeIds = new Set(cur.nodes.map(n => n.id));
const prevNodeIds = new Set((prev.nodes || []).map(n => n.id));
const new_nodes = [...curNodeIds].filter(id => !prevNodeIds.has(id));
const removed_nodes = [...prevNodeIds].filter(id => !curNodeIds.has(id));

let verdict;
if (new_bundled.length > 0) {
  verdict = `${new_bundled.length} new bundled note(s): ${new_bundled[0]}…`;
} else if (new_orphans.length > 0) {
  verdict = `${new_orphans.length} new orphan(s): ${new_orphans[0]}…`;
} else if (node_delta > 0 && orphan_delta <= 0 && bundled_delta <= 0) {
  verdict = `+${node_delta} notes wired in`;
} else if (edge_delta > 10) {
  verdict = `+${edge_delta} new edges`;
} else {
  verdict = `graph refreshed (${cs.nodes}n / ${cs.edges}e / ${cs.bundled || 0}b)`;
}

const out = {
  cur_stats: cs,
  prev_stats: ps,
  node_delta,
  edge_delta,
  orphan_delta,
  bundled_delta,
  new_orphans,
  resolved_orphans,
  new_bundled,
  resolved_bundled,
  new_nodes,
  removed_nodes,
  verdict_one_line: verdict,
};
console.log(JSON.stringify(out, null, 2));
