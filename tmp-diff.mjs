#!/usr/bin/env node
import { execFileSync } from 'node:child_process';
import { readFileSync } from 'node:fs';

const prev = JSON.parse(execFileSync('git', ['show', 'HEAD:notegraph.json'], { maxBuffer: 64 * 1024 * 1024 }).toString());
const curr = JSON.parse(readFileSync('notegraph.json', 'utf8'));

const prevOrphans = new Set(prev.nodes.filter(n => n.inDegree === 0 && n.outDegree === 0).map(n => n.id));
const currOrphans = new Set(curr.nodes.filter(n => n.inDegree === 0 && n.outDegree === 0).map(n => n.id));
const prevBundled = new Set(prev.nodes.filter(n => n.bundled === true).map(n => n.id));
const currBundled = new Set(curr.nodes.filter(n => n.bundled === true).map(n => n.id));

const newOrphans = [...currOrphans].filter(x => !prevOrphans.has(x));
const resolvedOrphans = [...prevOrphans].filter(x => !currOrphans.has(x));
const newBundled = [...currBundled].filter(x => !prevBundled.has(x));
const resolvedBundled = [...prevBundled].filter(x => !currBundled.has(x));

const nodeDelta = curr.stats.nodes - prev.stats.nodes;
const edgeDelta = curr.stats.edges - prev.stats.edges;
const orphanDelta = curr.stats.orphans - prev.stats.orphans;
const bundledDelta = (curr.stats.bundled ?? 0) - (prev.stats.bundled ?? 0);

let verdict;
if (newBundled.length > 0) {
  verdict = `${newBundled.length} new bundled note(s): ${newBundled[0]}…`;
} else if (newOrphans.length > 0) {
  verdict = `${newOrphans.length} new orphan(s): ${newOrphans[0]}…`;
} else if (nodeDelta > 0 && orphanDelta <= 0 && bundledDelta <= 0) {
  verdict = `+${nodeDelta} notes wired in`;
} else if (edgeDelta > 10) {
  verdict = `+${edgeDelta} new edges`;
} else {
  verdict = `graph refreshed (${curr.stats.nodes}n / ${curr.stats.edges}e / ${curr.stats.bundled ?? 0}b)`;
}

const bland = verdict.startsWith('graph refreshed') && newOrphans.length === 0 && resolvedOrphans.length === 0;

console.log(JSON.stringify({
  prev_stats: prev.stats,
  curr_stats: curr.stats,
  node_delta: nodeDelta,
  edge_delta: edgeDelta,
  orphan_delta: orphanDelta,
  bundled_delta: bundledDelta,
  new_orphans: newOrphans,
  resolved_orphans: resolvedOrphans,
  new_bundled: newBundled,
  resolved_bundled: resolvedBundled,
  verdict,
  bland_notify_suppression: bland,
}, null, 2));
