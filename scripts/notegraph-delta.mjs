import { readFileSync } from 'node:fs';
import { execSync } from 'node:child_process';

const head = JSON.parse(execSync('git show HEAD:notegraph.json', { maxBuffer: 100 * 1024 * 1024 }).toString());
const curr = JSON.parse(readFileSync('notegraph.json', 'utf8'));

const orphansOf = (j) => new Set(j.nodes.filter(n => n.inDegree === 0 && n.outDegree === 0).map(n => n.id));
const bundledOf = (j) => new Set(j.nodes.filter(n => n.bundled === true).map(n => n.id));

const headOrph = orphansOf(head);
const currOrph = orphansOf(curr);
const headBun = bundledOf(head);
const currBun = bundledOf(curr);

const diffSet = (a, b) => [...a].filter(x => !b.has(x));

const newOrphans = diffSet(currOrph, headOrph);
const resolvedOrphans = diffSet(headOrph, currOrph);
const newBundled = diffSet(currBun, headBun);
const resolvedBundled = diffSet(headBun, currBun);

const nodeDelta = curr.stats.nodes - head.stats.nodes;
const edgeDelta = curr.stats.edges - head.stats.edges;
const orphanDelta = curr.stats.orphans - head.stats.orphans;
const bundledDelta = (curr.stats.bundled ?? 0) - (head.stats.bundled ?? 0);

let verdict;
if (newBundled.length > 0) verdict = `${newBundled.length} new bundled note(s): ${newBundled[0]}…`;
else if (newOrphans.length > 0) verdict = `${newOrphans.length} new orphan(s): ${newOrphans[0]}…`;
else if (nodeDelta > 0 && orphanDelta <= 0 && bundledDelta <= 0) verdict = `+${nodeDelta} notes wired in`;
else if (edgeDelta > 10) verdict = `+${edgeDelta} new edges`;
else verdict = `graph refreshed (${curr.stats.nodes}n / ${curr.stats.edges}e / ${curr.stats.bundled ?? 0}b)`;

const out = {
  head_stats: head.stats,
  curr_stats: curr.stats,
  node_delta: nodeDelta,
  edge_delta: edgeDelta,
  hard_delta: curr.stats.hard - head.stats.hard,
  soft_delta: curr.stats.soft - head.stats.soft,
  orphan_delta: orphanDelta,
  bundled_delta: bundledDelta,
  atomic_delta: (curr.stats.atomic ?? 0) - (head.stats.atomic ?? 0),
  new_orphans: newOrphans,
  resolved_orphans: resolvedOrphans,
  new_bundled: newBundled,
  resolved_bundled: resolvedBundled,
  verdict_one_line: verdict,
};

console.log(JSON.stringify(out, null, 2));
