#!/usr/bin/env node
/**
 * find — semantic search across the repo's notes and (optionally) skills.
 *
 * Pure TF-IDF cosine: no embeddings, no API calls, no model. Same tokenizer
 * and stripping rules as scripts/notegraph.mjs and scripts/skillpacks.mjs.
 *
 * Usage:
 *   node scripts/find.mjs "fleet runner observability"
 *   node scripts/find.mjs --limit 5 "compute futures basket"
 *   node scripts/find.mjs --scope skills "vulnerability triage"
 *   node scripts/find.mjs --scope all --json "swarm safety"
 *
 * Flags
 *   --limit N        max results (default 10)
 *   --scope notes    only memory/ + docs/ (default)
 *   --scope skills   only skills/<slug>/SKILL.md
 *   --scope all      both
 *   --min S          minimum score threshold (default 0.05)
 *   --json           machine-readable output (one object per line as JSON)
 *
 * Exit codes
 *   0  results found
 *   1  no results above threshold
 *   2  bad usage
 */
import { readFileSync, existsSync } from "node:fs";
import { resolve, relative, basename } from "node:path";
import { fileURLToPath } from "node:url";
import { execFileSync } from "node:child_process";

const ROOT = resolve(fileURLToPath(new URL("..", import.meta.url)));

// ── argv ───────────────────────────────────────────────────────────────────
function parseArgv(argv) {
  const opts = { limit: 10, scope: "notes", min: 0.05, json: false, query: "" };
  const positional = [];
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === "--limit") opts.limit = Number(argv[++i]);
    else if (a === "--scope") opts.scope = argv[++i];
    else if (a === "--min") opts.min = Number(argv[++i]);
    else if (a === "--json") opts.json = true;
    else if (a === "-h" || a === "--help") opts.help = true;
    else positional.push(a);
  }
  opts.query = positional.join(" ").trim();
  return opts;
}

function usage(stream = process.stdout) {
  stream.write(
    `Usage: node scripts/find.mjs [--limit N] [--scope notes|skills|all] [--min S] [--json] "query terms"\n` +
    `\n` +
    `Examples:\n` +
    `  node scripts/find.mjs "fleet runner observability"\n` +
    `  node scripts/find.mjs --scope skills --limit 5 "vulnerability triage"\n` +
    `  node scripts/find.mjs --scope all --json "swarm safety"\n`,
  );
}

// ── corpus loaders (tracked-files only, same as notegraph + skillpacks) ───
function lsFiles(...patterns) {
  try {
    return execFileSync("git", ["ls-files", "--", ...patterns], { cwd: ROOT, encoding: "utf8", maxBuffer: 32 * 1024 * 1024 })
      .split("\n").filter(Boolean);
  } catch (err) {
    throw new Error(`find: git ls-files failed (${err.message})`);
  }
}

function loadNotes() {
  return lsFiles("memory/*.md", "memory/**/*.md", "docs/*.md", "docs/**/*.md")
    .filter((p) => !p.startsWith("memory/logs/"))
    .filter((p) => existsSync(resolve(ROOT, p)));
}

function loadSkills() {
  return lsFiles("skills/*/SKILL.md").filter((p) => existsSync(resolve(ROOT, p)));
}

// ── parsing — keep it tight; we don't need every field that notegraph reads ─
const RE_FRONTMATTER = /^---\n([\s\S]*?)\n---/;

function parseDoc(relPath, kind) {
  const raw = readFileSync(resolve(ROOT, relPath), "utf8");
  let body = raw;
  let title = kind === "skill" ? relPath.split("/")[1] : basename(relPath, ".md");
  const fm = raw.match(RE_FRONTMATTER);
  if (fm) {
    body = raw.slice(fm[0].length);
    const t = fm[1].match(/^name:\s*(.+)$/m) || fm[1].match(/^title:\s*(.+)$/m);
    if (t) title = t[1].trim().replace(/^["']|["']$/g, "");
  } else {
    const h1 = body.match(/^#\s+(.+)$/m);
    if (h1) title = h1[1].trim();
  }
  return { id: relPath, kind, title, body };
}

// ── tokenizer + stripping (same rules as notegraph / skillpacks) ──────────
const STOPWORDS = new Set((
  "a an and are as at be but by for from has have he her his how if in into is it its " +
  "of on or that the their they this to was we were what when where which who will with " +
  "you your i me my our us am do does did been being would could should may might can " +
  "not no nor so than then there here also any all each some such only just very more " +
  "most other than them these those one two three set use used using uses run runs " +
  "running ran via per eg ie etc"
).split(" "));

function stripBody(body) {
  return body
    .replace(/```[\s\S]*?```/g, "")
    .replace(/`[^`\n]+`/g, "")
    .replace(/<style[\s\S]*?<\/style>/gi, "")
    .replace(/<script[\s\S]*?<\/script>/gi, "")
    .replace(/<[^>]+>/g, " ")
    .replace(/style="[^"]*"/g, " ")
    .replace(/\{%[\s\S]*?%\}/g, " ")
    .replace(/\{\{[\s\S]*?\}\}/g, " ");
}

function tokenize(text) {
  const out = [];
  for (const raw of text.toLowerCase().split(/[^a-z0-9]+/)) {
    if (raw.length < 3 || raw.length > 30) continue;
    if (/^[0-9]+$/.test(raw)) continue;
    if (STOPWORDS.has(raw)) continue;
    out.push(raw);
  }
  return out;
}

// ── TF-IDF index + query scoring ──────────────────────────────────────────
function buildIndex(docs) {
  const tfs = docs.map((d) => {
    const tokens = tokenize(stripBody(d.body) + " " + d.title);
    const tf = new Map();
    for (const t of tokens) tf.set(t, (tf.get(t) || 0) + 1);
    return tf;
  });
  const df = new Map();
  for (const tf of tfs) for (const term of tf.keys()) df.set(term, (df.get(term) || 0) + 1);
  const N = docs.length;
  // Smoothed IDF: log(1 + N/df). Rare terms get a high weight (log(1+N) at
  // df=1) and terms that appear in nearly every doc get a meaningful nonzero
  // floor (~log(2) = 0.69) instead of zeroing out. Both edges matter:
  //   - without the floor, `./find --scope skills "skill"` ranks every hit
  //     below --min and looks empty even though every doc matches;
  //   - without keeping df=1 terms, unique identifiers users actually search
  //     for (codenames, commit hashes, error strings) return no matches.
  const idfFor = (dfTerm) => Math.log(1 + N / dfTerm);
  const vectors = tfs.map((tf) => {
    const v = new Map();
    let normSq = 0;
    for (const [term, count] of tf) {
      const dfTerm = df.get(term);
      const w = (1 + Math.log(count)) * idfFor(dfTerm);
      v.set(term, w);
      normSq += w * w;
    }
    return { v, norm: Math.sqrt(normSq) };
  });
  return { vectors, df, N, idfFor };
}

function scoreQuery(query, docs, index) {
  // Build a query vector with the same IDF as the index. Terms not seen in
  // the corpus contribute nothing; we report them so the user knows.
  const qTokens = tokenize(query);
  const qTf = new Map();
  for (const t of qTokens) qTf.set(t, (qTf.get(t) || 0) + 1);
  const qV = new Map();
  let qNormSq = 0;
  const unknown = [];
  for (const [term, count] of qTf) {
    const dfTerm = index.df.get(term);
    if (!dfTerm) { unknown.push(term); continue; }
    const w = (1 + Math.log(count)) * index.idfFor(dfTerm);
    qV.set(term, w);
    qNormSq += w * w;
  }
  const qNorm = Math.sqrt(qNormSq);

  const results = [];
  if (qNorm === 0) return { results, unknown };
  for (let i = 0; i < docs.length; i++) {
    const { v, norm } = index.vectors[i];
    if (norm === 0) continue;
    const [small, large] = qV.size < v.size ? [qV, v] : [v, qV];
    let dot = 0;
    const matched = [];
    for (const [term, w] of small) {
      const w2 = large.get(term);
      if (w2 !== undefined) { dot += w * w2; matched.push([term, w * w2]); }
    }
    if (dot === 0) continue;
    const score = dot / (qNorm * norm);
    matched.sort((a, b) => b[1] - a[1]);
    results.push({
      id: docs[i].id,
      kind: docs[i].kind,
      title: docs[i].title,
      score: Math.round(score * 1000) / 1000,
      matched: matched.slice(0, 5).map(([t]) => t),
    });
  }
  results.sort((a, b) => b.score - a.score);
  return { results, unknown };
}

// ── output formatters ──────────────────────────────────────────────────────
function formatTty(opts, hits, unknown) {
  if (hits.length === 0) {
    if (unknown.length === opts._totalQueryTerms) {
      process.stderr.write(`No matches. None of the query terms appear in the corpus: ${unknown.join(", ")}\n`);
    } else if (unknown.length > 0) {
      process.stderr.write(`No matches above --min ${opts.min}. Unknown query terms (not in corpus): ${unknown.join(", ")}\n`);
    } else {
      process.stderr.write(`No matches above --min ${opts.min}.\n`);
    }
    return;
  }
  // pad columns
  const titleW = Math.min(40, Math.max(...hits.map((h) => h.title.length)));
  for (const h of hits) {
    const kindBadge = h.kind === "skill" ? "skl" : "nte";
    const title = h.title.length > titleW ? h.title.slice(0, titleW - 1) + "…" : h.title.padEnd(titleW);
    process.stdout.write(
      `  ${h.score.toFixed(3)}  [${kindBadge}]  ${title}  ${h.id}  [${h.matched.join(", ")}]\n`,
    );
  }
  if (unknown.length > 0) {
    process.stderr.write(`\n(unknown query terms — df<2 in corpus: ${unknown.join(", ")})\n`);
  }
}

function formatJson(hits) {
  for (const h of hits) process.stdout.write(JSON.stringify(h) + "\n");
}

// ── main ───────────────────────────────────────────────────────────────────
function main() {
  const opts = parseArgv(process.argv.slice(2));
  if (opts.help) { usage(); process.exit(0); }
  if (!opts.query) { usage(process.stderr); process.exit(2); }
  if (!["notes", "skills", "all"].includes(opts.scope)) {
    process.stderr.write(`Bad --scope: ${opts.scope}\n`); process.exit(2);
  }

  const corpus = [];
  if (opts.scope === "notes" || opts.scope === "all") {
    for (const p of loadNotes()) corpus.push(parseDoc(p, "note"));
  }
  if (opts.scope === "skills" || opts.scope === "all") {
    for (const p of loadSkills()) corpus.push(parseDoc(p, "skill"));
  }
  if (corpus.length === 0) {
    process.stderr.write(`find: empty corpus (scope=${opts.scope})\n`); process.exit(1);
  }

  const index = buildIndex(corpus);
  const { results, unknown } = scoreQuery(opts.query, corpus, index);
  opts._totalQueryTerms = tokenize(opts.query).length;
  const filtered = results.filter((r) => r.score >= opts.min).slice(0, opts.limit);

  if (opts.json) formatJson(filtered);
  else formatTty(opts, filtered, unknown);

  process.exit(filtered.length > 0 ? 0 : 1);
}

main();
