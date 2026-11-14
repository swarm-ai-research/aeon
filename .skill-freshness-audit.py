#!/usr/bin/env python3
import os, re, json, hashlib, time
from datetime import datetime, timezone

BASE = "/home/runner/work/aeon/aeon"
TODAY = "2026-11-14"
NOW_EPOCH = int(time.time())

# Producer cadence from aeon.yml (derived earlier)
# daily = fires every day; weekly = fires once per week; on_demand = no expected cadence
CADENCE = {
    "planner": "daily",
    "batch-health": "daily",
    "memory-flush": "daily",  # every other day but still daily-class
    "memory-structural-dedupe": "daily",
    "stale-content-pr-sweeper": "daily",
    "issue-triage": "daily",
    "pr-triage": "daily",
    "pr-review": "daily",
    "pr-tracker": "daily",
    "github-monitor": "daily",
    "code-health": "daily",
    "surplus-pulse": "daily",
    "compute-futures-eda": "daily",
    "goal-tracker": "daily",
    "skill-health": "daily",
    "reflect": "daily",
    "fleet-control": "daily",
    "gitlawb-fleet-metrics": "daily",
    "notegraph": "daily",
    "suggest-edges": "daily",
    "skill-freshness": "daily",
    "run-frequency-guard": "daily",
    "heartbeat": "daily",
    "janitor": "weekly",
    "repo-revive": "weekly",
    "compute-pulse": "weekly",
    "compute-macro-correlate": "weekly",
    "changelog": "weekly",
    "vuln-scanner": "weekly",
    "agi-tracker": "weekly",
    "milestone-tracker": "weekly",
    "config-validator": "weekly",
    "skill-analytics": "weekly",
    "self-review": "weekly",
    "cost-report": "weekly",
    "ai-framework-watch": "weekly",
    "skill-evals": "weekly",
    "swarm-safety-eval": "weekly",
    "skill-update-check": "weekly",
    "weekly-shiplog": "weekly",
    "workflow-security-audit": "weekly",
    "skill-graph": "weekly",
    "skillpacks": "weekly",
    "skill-repair": "on_demand",
}

def path_class(path):
    if path.startswith("articles/"):
        return "articles"
    elif path.startswith(".outputs/"):
        return "outputs"
    elif path.startswith("memory/topics/"):
        return "topics"
    elif path.startswith("memory/state/"):
        return "state"
    return "unknown"

def threshold_hours(pclass, producer_cadence):
    if pclass == "articles":
        return 28 if producer_cadence == "daily" else 192
    elif pclass == "outputs":
        return 4
    elif pclass == "topics":
        return 168
    elif pclass == "state":
        return 720
    return 168

def producer_from_path(path):
    """Guess the producer skill name from the path."""
    if path.startswith("articles/"):
        name = path[len("articles/"):]
        # Remove suffixes
        name = re.sub(r'-\$\{today\}\.md$', '', name)
        name = re.sub(r'-[0-9]{4}-[0-9]{2}-[0-9]{2}\.md$', '', name)
        name = re.sub(r'-\*\.md$', '', name)
        name = re.sub(r'\.md$', '', name)
        return name
    return None

def resolve_path(path):
    """Resolve a path pattern to an actual file on disk."""
    full = os.path.join(BASE, path)
    if "${today}" in path:
        # canonical today pattern - check if today's file exists
        actual = path.replace("${today}", TODAY)
        full_actual = os.path.join(BASE, actual)
        if os.path.exists(full_actual):
            return actual, True
        # Find most recent
        prefix = path.split("${today}")[0]  # e.g. "articles/fleet-status-"
        glob_base = os.path.join(BASE, os.path.dirname(prefix))
        prefix_name = os.path.basename(prefix)
        try:
            files = sorted([f for f in os.listdir(glob_base) if f.startswith(prefix_name)], reverse=True)
            if files:
                return os.path.join(os.path.dirname(prefix), files[0]), True
        except:
            pass
        return actual, False  # canonical, doesn't exist
    elif "*" in path:
        # wildcard - find most recent
        prefix = path.split("*")[0]  # e.g. "articles/fleet-status-"
        glob_base = os.path.join(BASE, os.path.dirname(prefix))
        prefix_name = os.path.basename(prefix)
        try:
            files = sorted([f for f in os.listdir(glob_base) if f.startswith(prefix_name) and f.endswith(".md")], reverse=True)
            if files:
                actual = os.path.join(os.path.dirname(prefix), files[0])
                return actual, os.path.exists(os.path.join(BASE, actual))
        except:
            pass
        return path, False  # doesn't exist
    else:
        return path, os.path.exists(full)

def get_mtime(path):
    full = os.path.join(BASE, path)
    try:
        return os.path.getmtime(full)
    except:
        return None

def score_severity(age_hours, threshold_hours):
    if age_hours <= threshold_hours:
        return "OK"
    elif age_hours <= 2 * threshold_hours:
        return "WARN"
    else:
        return "STALE"

SEVERITY_RANK = {"OK": 0, "WARN": 1, "STALE": 2, "MISSING": 3}

# Raw dependencies from scan (manual filter of obvious self-refs and examples)
raw_deps = [
    ("planner", "memory/state/planner-state.json"),
    ("memory-flush", "memory/topics/skills-history.md"),
    ("stale-content-pr-sweeper", "memory/state/notegraph.json"),
    ("pr-review", "memory/topics/pr-review-rules.md"),
    ("pr-tracker", "memory/topics/pr-status.md"),
    ("surplus-pulse", "memory/topics/projects.md"),
    ("surplus-pulse", "memory/topics/surplus-pulse.md"),
    # fleet-control reads fleet-status articles it previously wrote (self-state-keeping) - filter
    # fleet-control also uses fleet-control-state.json
    ("fleet-control", "memory/state/fleet-control-state.json"),
    ("notegraph", "memory/state/notegraph.json"),
    ("suggest-edges", "memory/state/suggest-edges.json"),
    # skill-freshness examples (foo-2026, repo-pulse, token-report) - implicit, treat as ignored
    # heartbeat token-report references - check if real
    ("heartbeat", "articles/token-report-*.md"),
    # repo-revive
    ("repo-revive", "memory/topics/stale-models.md"),
    ("repo-revive", "memory/topics/watched-repos.md"),
    # compute-pulse
    ("compute-pulse", "memory/topics/compute-pulse.md"),
    ("compute-pulse", "memory/topics/compute-tokens.md"),
    # compute-macro-correlate
    ("compute-macro-correlate", "memory/topics/compute-futures-macro-correlations.md"),
    # vuln-scanner reads github-trending output
    ("vuln-scanner", ".outputs/github-trending.md"),
    # vuln-scanner articles/vuln-scan-${today}.md - skip (self-referential: vuln-scanner writes vuln-scan*)
    # weekly-shiplog
    ("weekly-shiplog", "articles/push-recap-*.md"),
    # skillpacks
    ("skillpacks", "memory/state/skillpacks.json"),
    # skill-repair
    ("skill-repair", "memory/state/skill-repair-history.json"),
]

# Also add fleet-control article dep (not self-ref since prefix "fleet-status" != "fleet-control")
raw_deps.append(("fleet-control", "articles/fleet-status-${today}.md"))

results = []  # (consumer, resolved_path, pclass, age_hours, threshold, severity, exists)
ignored_count = 0

for consumer, dep_path in raw_deps:
    # Resolve path
    resolved, exists = resolve_path(dep_path)
    pclass = path_class(dep_path)

    # Determine producer cadence
    producer = producer_from_path(dep_path)
    prod_cadence = CADENCE.get(producer, "daily") if producer else "daily"
    # For state/topics, cadence doesn't matter for threshold
    thresh = threshold_hours(pclass, prod_cadence)

    if not exists:
        # Check if this should be MISSING (explicit/canonical) or just ignored (implicit that never existed)
        is_canonical_today = "${today}" in dep_path
        is_explicit = False  # no chains: consume: edges

        if is_canonical_today or is_explicit:
            severity = "MISSING"
            results.append((consumer, dep_path, pclass, None, thresh, severity))
        else:
            # implicit wildcard that doesn't exist - skip/ignore
            ignored_count += 1
        continue

    mtime = get_mtime(resolved)
    if mtime is None:
        ignored_count += 1
        continue

    age_hours = (NOW_EPOCH - mtime) / 3600
    severity = score_severity(age_hours, thresh)
    results.append((consumer, dep_path, pclass, age_hours, thresh, severity))

# De-duplicate fleet-control articles (fleet-status-${today} and fleet-status-* are same)
seen = set()
deduped = []
for r in results:
    consumer, dep, pclass, age, thresh, sev = r
    key = (consumer, dep.split("*")[0].split("${today}")[0])
    if key not in seen:
        seen.add(key)
        deduped.append(r)
results = deduped

# Aggregate per-consumer
consumer_verdicts = {}
for consumer, dep, pclass, age, thresh, sev in results:
    cur = consumer_verdicts.get(consumer, {"severity": "OK", "deps": []})
    cur["deps"].append((dep, pclass, age, thresh, sev))
    if SEVERITY_RANK.get(sev, 0) > SEVERITY_RANK.get(cur["severity"], 0):
        cur["severity"] = sev
    consumer_verdicts[consumer] = cur

# Fleet verdict
fleet_verdict = "FRESHNESS_OK"
worst_sev = "OK"
for c, v in consumer_verdicts.items():
    if SEVERITY_RANK.get(v["severity"], 0) > SEVERITY_RANK.get(worst_sev, 0):
        worst_sev = v["severity"]

if worst_sev in ("STALE", "MISSING"):
    fleet_verdict = "FRESHNESS_STALE"
elif worst_sev == "WARN":
    fleet_verdict = "FRESHNESS_WARN"

# Count stats
enabled_count = len(CADENCE)
dep_count = len(results)
flagged = [(c, d, p, a, t, s) for c, d, p, a, t, s in results if s != "OK"]
flagged_count = len(flagged)

# Fingerprint
fingerprint_input = "\n".join(sorted(f"{c}:{d}:{s}" for c, d, p, a, t, s in results if s != "OK"))
fingerprint = hashlib.sha1(fingerprint_input.encode()).hexdigest()

# Prior state
PRIOR_FINGERPRINT = "da39a3ee5e6b4b0d3255bfef95601890afd80709"
PRIOR_VERDICT = "FRESHNESS_OK"
prior_run_at = "2026-11-13T08:46:59Z"

# Notify decision
prior_run_epoch = 1731490019  # 2026-11-13T08:46:59Z approx
days_since_prior = (NOW_EPOCH - prior_run_epoch) / 86400

if fleet_verdict == "FRESHNESS_OK":
    notify_decision = "no — FRESHNESS_OK"
elif fingerprint == PRIOR_FINGERPRINT and days_since_prior < 7:
    notify_decision = "no — FRESHNESS_NO_CHANGE"
    fleet_verdict_final = "FRESHNESS_NO_CHANGE"
else:
    notify_decision = "yes"

fleet_verdict_final = fleet_verdict

# Human age formatter
def fmt_age(hours):
    if hours is None:
        return "N/A"
    if hours < 48:
        return f"{hours:.0f}h"
    return f"{hours/24:.1f}d"

# Verdict emoji
def verdict_emoji(sev):
    return {"OK": "✅", "WARN": "⚠️", "STALE": "🔴", "MISSING": "❌",
            "FRESHNESS_OK": "✅", "FRESHNESS_WARN": "⚠️", "FRESHNESS_STALE": "🔴", "FRESHNESS_NO_CHANGE": "✅"}.get(sev, "")

# Build article
flagged_sorted = sorted(flagged, key=lambda x: (-SEVERITY_RANK.get(x[5], 0), x[0]))
ok_consumers = [c for c in consumer_verdicts if consumer_verdicts[c]["severity"] == "OK"]

# one-line summary
if fleet_verdict_final in ("FRESHNESS_OK", "FRESHNESS_NO_CHANGE"):
    one_line = f"all {dep_count} dependencies fresh across {enabled_count} enabled consumers"
elif fleet_verdict_final == "FRESHNESS_WARN":
    one_line = f"{flagged_count} of {dep_count} deps past threshold (no STALE/MISSING)"
else:
    one_line = f"{flagged_count} of {dep_count} deps flagged ({worst_sev}) — attention needed"

article_lines = [
    f"# Skill Freshness — {TODAY}",
    "",
    f"**Verdict:** {verdict_emoji(fleet_verdict_final)} {fleet_verdict_final} — {one_line}",
    "",
    f"*Audited {enabled_count} enabled skills · {dep_count} dependencies checked · {flagged_count} flagged*",
    "",
]

if flagged_count > 0:
    article_lines += [
        "## Flagged dependencies",
        "",
        "| Consumer | Dependency | Class | Age | Severity |",
        "|----------|-----------|-------|-----|----------|",
    ]
    for consumer, dep, pclass, age, thresh, sev in flagged_sorted:
        emoji = verdict_emoji(sev)
        article_lines.append(f"| {consumer} | `{dep}` | {pclass} | {fmt_age(age)} | {emoji} {sev} |")
    article_lines.append("")

    article_lines.append("## What this means per consumer")
    article_lines.append("")
    for consumer in sorted(set(c for c, d, p, a, t, s in flagged_sorted)):
        v = consumer_verdicts[consumer]
        worst_dep = max(v["deps"], key=lambda x: SEVERITY_RANK.get(x[4], 0))
        wpath, wpclass, wage, wthresh, wsev = worst_dep
        producer = producer_from_path(wpath)
        if wsev == "MISSING":
            suggestion = f"Check `{producer or '?'}` run history with `./scripts/skill-runs --skill {producer or '?'} --hours 168`." if producer else "File never created on disk."
        elif wsev == "STALE":
            suggestion = f"Verify `{producer or '?'}` is still on schedule; if so, the producer ran but did not write a new article."
        else:
            suggestion = "Monitor — one missed run, expected to clear on next producer cadence."
        article_lines.append(f"> **{consumer}** — depends on {len(v['deps'])} file(s); {sum(1 for d in v['deps'] if d[4] != 'OK')} flagged. Worst: `{wpath}` last updated {fmt_age(wage)} ago (threshold {wthresh}h, class {wpclass}). Suggested action: {suggestion}")
        article_lines.append("")
else:
    article_lines += [
        "## Flagged dependencies",
        "",
        "*None — all dependencies are fresh.*",
        "",
    ]

article_lines += [
    "## Healthy consumers",
    "",
]
shown = 0
for c in sorted(ok_consumers):
    v = consumer_verdicts.get(c, {"deps": []})
    dep_cnt = len(v["deps"])
    article_lines.append(f"- {c} — {dep_cnt} dep(s), all fresh.")
    shown += 1
    if shown >= 8:
        rest = len(ok_consumers) - shown
        if rest > 0:
            article_lines.append(f"+ {rest} more all-fresh consumers.")
        break

# Count consumers not in consumer_verdicts (they have 0 deps discovered)
no_dep_consumers = [s for s in CADENCE if s not in consumer_verdicts]
if no_dep_consumers:
    article_lines.append(f"+ {len(no_dep_consumers)} more enabled consumers with no discovered file dependencies (all assumed fresh).")

article_lines += [
    "",
    "## Source status",
    "",
    f"- `aeon.yml`: {enabled_count} enabled entries parsed",
    f"- Implicit references discovered: {dep_count}",
    f"- Explicit `chains: consume:` edges: 0 (chains block is commented out)",
    f"- Files not yet on disk (skipped — implicit references that never existed): {ignored_count}",
    "",
    "---",
    "*Companion to `skill-health` (per-skill failure detection) and `heartbeat` (per-run pulse). This skill catches the silent-staleness gap those two cannot: a consumer reading a stale file with no API errors and a 100% pass rate. Methodology: every age and threshold is computed from on-disk mtimes — this skill measures nothing it does not also report.*",
]

article_content = "\n".join(article_lines)

# Write article
article_path = os.path.join(BASE, f"articles/skill-freshness-{TODAY}.md")
with open(article_path, "w") as f:
    f.write(article_content)
print(f"ARTICLE_WRITTEN: {article_path}")

# Update state
state = {
    "last_run_at": datetime.fromtimestamp(NOW_EPOCH, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "last_verdict": fleet_verdict_final,
    "last_flagged_fingerprint": fingerprint,
    "consumer_count": enabled_count,
    "dependency_count": dep_count,
    "flagged_count": flagged_count,
    "first_seen_at": {}
}
# Carry over first_seen_at from prior state for still-flagged items
# (prior first_seen_at was empty, so nothing to carry)

state_path = os.path.join(BASE, "memory/topics/skill-freshness-state.json")
with open(state_path, "w") as f:
    json.dump(state, f, indent=2)
print(f"STATE_WRITTEN: {state_path}")

# Print summary for notification building
print(f"FLEET_VERDICT: {fleet_verdict_final}")
print(f"FLAGGED_COUNT: {flagged_count}")
print(f"DEP_COUNT: {dep_count}")
print(f"ENABLED_COUNT: {enabled_count}")
print(f"NOTIFY_DECISION: {notify_decision}")
print(f"FINGERPRINT: {fingerprint}")
print(f"IGNORED_COUNT: {ignored_count}")
print(f"NOW_EPOCH: {NOW_EPOCH}")
print(f"WORST_SEV: {worst_sev}")

# Print flagged items for notification
for consumer, dep, pclass, age, thresh, sev in flagged_sorted[:5]:
    print(f"FLAGGED_ITEM: {consumer} <- {dep} ({fmt_age(age)} old, class {pclass}, sev {sev})")
