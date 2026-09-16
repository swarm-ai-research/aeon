#!/usr/bin/env node
import { readFileSync } from 'fs';
import { execSync } from 'child_process';

const cur = JSON.parse(readFileSync('notegraph.json', 'utf8'));
const prev = JSON.parse(execSync('git show HEAD:notegraph.json').toString());

function nodeMap(g) {
  const m = new Map();
  for (const n of g.nodes) m.set(n.id, n);
  return m;
}
const curMap = nodeMap(cur);
const prevMap = nodeMap(prev);

function isOrphan(n) {
  return (n.inDegree === 0 && n.outDegree === 0);
}

const new_orphans = [];
const resolved_orphans = [];
const new_bundled = [];
const resolved_bundled = [];

for (const [id, n] of curMap) {
  const p = prevMap.get(id);
  if (isOrphan(n) && !(p && isOrphan(p))) new_orphans.push(id);
  if (n.bundled && !(p && p.bundled)) new_bundled.push(id);
}
for (const [id, p] of prevMap) {
  const c = curMap.get(id);
  if (isOrphan(p) && !(c && isOrphan(c))) resolved_orphans.push(id);
  if (p.bundled && !(c && c.bundled)) resolved_bundled.push(id);
}

const node_delta = cur.stats.nodes - prev.stats.nodes;
const edge_delta = cur.stats.edges - prev.stats.edges;
const orphan_delta = cur.stats.orphans - prev.stats.orphans;
const bundled_delta = (cur.stats.bundled || 0) - (prev.stats.bundled || 0);

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
  verdict = `graph refreshed (${cur.stats.nodes}n / ${cur.stats.edges}e / ${cur.stats.bundled || 0}b)`;
}

console.log(JSON.stringify({
  verdict,
  node_delta, edge_delta, orphan_delta, bundled_delta,
  new_orphans, resolved_orphans, new_bundled, resolved_bundled,
  stats: cur.stats,
  prev_stats: prev.stats,
}, null, 2));
