import hashlib

flagged = [
    ("ai-framework-watch", ".outputs/ai-framework-watch.md", "MISSING"),
    ("run-frequency-guard", ".outputs/run-frequency-guard.md", "MISSING"),
    ("memory-structural-dedupe", ".outputs/memory-structural-dedupe.md", "STALE"),
    ("memory-flush", ".outputs/memory-flush.md", "STALE"),
    ("gitlawb-fleet-metrics", ".outputs/gitlawb-fleet-metrics.md", "STALE"),
    ("batch-health", ".outputs/batch-health.md", "STALE"),
    ("heartbeat", ".outputs/heartbeat.md", "STALE"),
    ("skill-freshness", ".outputs/skill-freshness.md", "STALE"),
    ("fleet-control", ".outputs/fleet-control.md", "STALE"),
    ("issue-triage", ".outputs/issue-triage.md", "STALE"),
    ("github-monitor", ".outputs/github-monitor.md", "STALE"),
    ("pr-triage", ".outputs/pr-triage.md", "STALE"),
    ("repo-revive", ".outputs/repo-revive.md", "WARN"),
    ("compute-pulse", ".outputs/compute-pulse.md", "WARN"),
    ("skillpacks", ".outputs/skillpacks.md", "WARN"),
    ("config-validator", ".outputs/config-validator.md", "WARN"),
    ("compute-macro-correlate", ".outputs/compute-macro-correlate.md", "WARN"),
    ("swarm-safety-eval", ".outputs/swarm-safety-eval.md", "WARN"),
    ("skill-evals", ".outputs/skill-evals.md", "WARN"),
    ("planner", ".outputs/planner.md", "WARN"),
    ("compute-futures-eda", ".outputs/compute-futures-eda.md", "WARN"),
    ("code-health", ".outputs/code-health.md", "WARN"),
    ("surplus-pulse", ".outputs/surplus-pulse.md", "WARN"),
    ("suggest-edges", ".outputs/suggest-edges.md", "WARN"),
    ("notegraph", ".outputs/notegraph.md", "WARN"),
]

triples = sorted(f"{c}:{d}:{s}" for c, d, s in flagged)
fingerprint = hashlib.sha1("\n".join(triples).encode()).hexdigest()
print(f"Fingerprint: {fingerprint}")
print(f"Triples ({len(triples)}):")
for t in triples:
    print(f"  {t}")
