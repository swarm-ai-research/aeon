import { readFileSync } from 'node:fs';
import { execSync } from 'node:child_process';

const cur = JSON.parse(readFileSync('notegraph.json', 'utf8'));
const prevRaw = execSync('git show HEAD:notegraph.json', { encoding: 'utf8' });
const prev = JSON.parse(prevRaw);

const nodeDelta = cur.stats.nodes - prev.stats.nodes;
const edgeDelta = cur.stats.edges - prev.stats.edges;
const orphanDelta = cur.stats.orphans - prev.stats.orphans;
const bundledDelta = (cur.stats.bundled ?? 0) - (prev.stats.bundled ?? 0);

function orphanSet(g) {
  const s = new Set();
  for (const n of g.nodes) {
    const inD = n.inDegree ?? 0;
    const outD = n.outDegree ?? 0;
    if (inD === 0 && outD === 0) s.add(n.id);
  }
  return s;
}
function bundledSet(g) {
  const s = new Set();
  for (const n of g.nodes) {
    if (n.bundled === true) s.add(n.id);
  }
  return s;
}

const prevOrphans = orphanSet(prev);
const curOrphans = orphanSet(cur);
const newOrphans = [...curOrphans].filter(id => !prevOrphans.has(id));
const resolvedOrphans = [...prevOrphans].filter(id => !curOrphans.has(id));

const prevBundled = bundledSet(prev);
const curBundled = bundledSet(cur);
const newBundled = [...curBundled].filter(id => !prevBundled.has(id));
const resolvedBundled = [...prevBundled].filter(id => !curBundled.has(id));

let verdict;
if (newBundled.length > 0) {
  verdict = `${newBundled.length} new bundled note(s): ${newBundled[0]}${newBundled.length>1?'…':''}`;
} else if (newOrphans.length > 0) {
  verdict = `${newOrphans.length} new orphan(s): ${newOrphans[0]}${newOrphans.length>1?'…':''}`;
} else if (nodeDelta > 0 && orphanDelta <= 0 && bundledDelta <= 0) {
  verdict = `+${nodeDelta} notes wired in`;
} else if (edgeDelta > 10) {
  verdict = `+${edgeDelta} new edges`;
} else {
  verdict = `graph refreshed (${cur.stats.nodes}n / ${cur.stats.edges}e / ${cur.stats.bundled ?? 0}b)`;
}

const out = {
  prev_stats: prev.stats,
  cur_stats: cur.stats,
  node_delta: nodeDelta,
  edge_delta: edgeDelta,
  orphan_delta: orphanDelta,
  bundled_delta: bundledDelta,
  new_orphans: newOrphans,
  resolved_orphans: resolvedOrphans,
  new_bundled: newBundled,
  resolved_bundled: resolvedBundled,
  verdict,
};
process.stdout.write(JSON.stringify(out, null, 2) + '\n');
