#!/usr/bin/env node
import { readFileSync, writeFileSync } from 'node:fs';
import { execSync } from 'node:child_process';

const current = JSON.parse(readFileSync('notegraph.json', 'utf8'));

let previous;
try {
  const raw = execSync('git show HEAD:notegraph.json', { encoding: 'utf8' });
  previous = JSON.parse(raw);
} catch (e) {
  previous = null;
  console.error('HEAD:notegraph.json unavailable');
}

const cur = current.stats;
const prev = previous ? previous.stats : { nodes: 0, edges: 0, hard: 0, soft: 0, orphans: 0, bundled: 0, atomic: 0 };

const node_delta = cur.nodes - prev.nodes;
const edge_delta = cur.edges - prev.edges;
const orphan_delta = (cur.orphans || 0) - (prev.orphans || 0);
const bundled_delta = (cur.bundled || 0) - (prev.bundled || 0);

function orphanSet(g) {
  if (!g) return new Set();
  const s = new Set();
  for (const [id, node] of Object.entries(g.nodes || {})) {
    if ((node.inDegree || 0) === 0 && (node.outDegree || 0) === 0) s.add(id);
  }
  return s;
}
function bundledSet(g) {
  if (!g) return new Set();
  const s = new Set();
  for (const [id, node] of Object.entries(g.nodes || {})) {
    if (node.bundled) s.add(id);
  }
  return s;
}

const curOrphans = orphanSet(current);
const prevOrphans = orphanSet(previous);
const curBundled = bundledSet(current);
const prevBundled = bundledSet(previous);

const new_orphans = [...curOrphans].filter(x => !prevOrphans.has(x));
const resolved_orphans = [...prevOrphans].filter(x => !curOrphans.has(x));
const new_bundled = [...curBundled].filter(x => !prevBundled.has(x));
const resolved_bundled = [...prevBundled].filter(x => !curBundled.has(x));

let verdict;
if (new_bundled.length > 0) verdict = `${new_bundled.length} new bundled note(s): ${new_bundled[0]}…`;
else if (new_orphans.length > 0) verdict = `${new_orphans.length} new orphan(s): ${new_orphans[0]}…`;
else if (node_delta > 0 && orphan_delta <= 0 && bundled_delta <= 0) verdict = `+${node_delta} notes wired in`;
else if (edge_delta > 10) verdict = `+${edge_delta} new edges`;
else verdict = `graph refreshed (${cur.nodes}n / ${cur.edges}e / ${cur.bundled}b)`;

const report = {
  verdict_one_line: verdict,
  cur,
  prev,
  node_delta, edge_delta, orphan_delta, bundled_delta,
  new_orphans, resolved_orphans, new_bundled, resolved_bundled,
};

console.log(JSON.stringify(report, null, 2));
writeFileSync('.notegraph-verdict.json', JSON.stringify(report, null, 2));
