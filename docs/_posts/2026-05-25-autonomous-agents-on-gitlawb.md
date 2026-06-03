---
title: "We Spawned Autonomous Agents on GitLawb. Here's What Happened."
date: 2026-05-25
author: rsavitt
layout: post
---

We spawned four autonomous agents on the GitLawb decentralized git node, gave them real tasks, and watched them work. This is what we learned about building agent fleets on a platform where your identity *is* your address.

## The Setup

GitLawb is a decentralized, agent-first git platform — no central authority, no GitHub, no OAuth. Each actor (human or agent) is a pure Ed25519 keypair identified by a `did:key`. Capabilities are granted via UCAN tokens with mandatory TTLs and delegation chains. The node at `node.gitlawb.com` runs the git protocol, task queue, and MCP server.

We had two PRs already in progress:

- **PR #3** — A complete safety/capability-lifecycle prototype: UCAN tokens with enforced chain-walk verification, a `CapabilityGuard` that clamps TTLs on safety-critical operations to 5 minutes, gated renewal (authority must be continuously re-earned), and a kill-switch via blocklist.
- **PR #4** — Hardening: fail-closed policy for missing activity data, explicit resource scoping for repo-mutating capabilities, and prevention of capability escalation on renewal.

The question was: can we take this from a prototype to real agents doing real work?

## Spawning the Fleet

Four agents, each with least-privilege capabilities:

```
aeon-researcher  — git:fetch, issue:create        (read + track)
aeon-reviewer    — git:fetch, pr:open, pr:review   (read + review)
aeon-deployer    — git:push, pr:merge, agent:deploy (write + merge, 5min TTL)
aeon-sentinel    — repo:admin, agent:deploy         (full audit, 5min TTL)
```

Each agent got its own Ed25519 keypair at `~/.gitlawb/fleet/<role>/identity.pem`. Registered via `gl register --dir <identity-dir> --capabilities <caps>`. The operator identity (root of trust) could delegate to any of them via `gl ucan delegate`.

**Key learning:** The `gl` CLI is the right interface. The `git-remote-gitlawb` helper handles git protocol auth automatically — URLs are `gitlawb://<did>/<repo-name>`, not hostnames. Your DID *is* your address.

## The Runner

We built `prototypes/gitlawb-safety/task-runner.mjs` — a polling runner that:

1. Reads agents from `memory/instances.json`
2. Polls `gl task list --assignee-did <did> --status pending`
3. Claims tasks with each agent's identity directory
4. Executes work (built-in prototype executors or shell hooks)
5. Persists artifacts to `memory/gitlawb-runner/`
6. Completes or fails the task back to GitLawb

Supports `once`/`loop` modes, `--dry-run` with fixture files, and per-agent filtering.

**Key learning:** Tasks must be created by the operator with `--assignee-did <agent>`. When an agent creates a task for itself, the node reassigns it to the operator. The `delegator_did` field is what preserves the assignment. This is correct behavior — delegation flows from principal to agent, not self-assignment.

## What the Agents Actually Did

| Agent | Task | What Happened |
|-------|------|---------------|
| **researcher** | Analyze fleet safety patterns | Read the guard and caps modules, counted 2 SAFETY_CRITICAL cap references, 15 lines of renewal logic, 9 chain verification paths. Produced a structured analysis. |
| **reviewer** | Review the autonomous fleet demo | Scanned 353 lines, found 15 potential hardcoded secrets (false positives — they're DID strings, not API keys), verified temp state isolation and observability wiring. Verdict: ISSUES (with caveats). |
| **deployer** | Prepare fleet-metrics deployment | Confirmed the fleet-metrics skill exists, CLI hook is wired, notify path is ready. Created a branch with integration code. |
| **sentinel** | Full security audit | Scanned for `rm -rf /` (found 6 — all in docs/AGENTS.md safety rules), private key refs (2 — the identity files). Verified attenuation enforcement: PASS. Renewal escalation check: PASS. Fail-closed on missing activity: PASS. Self-modification block: PASS. Blocklist mechanism: PASS. Risk: MEDIUM. |

Each agent's work was persisted as a JSON artifact in `memory/gitlawb-runner/` with the full task, instance metadata, result, and timestamp.

## What We Learned

### 1. Authority must be continuously re-earned

The safety layer's core insight: stop renewing → the instance goes dark. Safety-critical caps (agent/deploy, repo/admin, pr/merge) get 5-minute TTLs. The guard's `renew()` method checks that the prior token is authentic, not revoked, and that the agent's recent activity passes a policy check. Touch the safety machinery itself? Renewal denied. No coordination needed — the token simply ceases to exist.

### 2. The kill-switch works differently than you'd expect

Blocklisting a DID doesn't revoke its token — it adds an immediate deny to the authorization check. The sentinel could still hold a valid token, but `guard.authorize()` returns `denied_by_blocklist` instantly. No TTL wait. No coordination. The token becomes inert.

### 3. Least-privilege is the multiplier

The more agents you spawn, the more the safety layer matters. Each agent gets exactly the capabilities it needs — the researcher can't merge, the reviewer can't push, the deployer can't audit. If a researcher gets compromised, the blast radius is limited to creating issues. Escalation attempts are caught at the authorization layer.

### 4. GitLawb's task system is the coordination primitive

The task queue is simple: `create → pending → claim → complete/fail`. Tasks carry a `kind`, a JSON `payload`, and a `capability` requirement. The operator creates tasks with `--assignee-did` to delegate. Agents claim and execute. Results flow back as structured data. No pub/sub, no webhooks, no polling loops over HTTP — just the `gl` CLI talking to the node.

### 5. The `did:key` addressing model changes everything

No usernames, no emails, no OAuth tokens. Each agent is a cryptographic identity. The git remote URL is `gitlawb://did:key:z6Mk.../aeon`. Auth is automatic via the Ed25519 key in `~/.gitlawb/identity.pem`. This means agents can be created, destroyed, and delegated to without touching any central user database. Identity is pure crypto.

### 6. The prototype executors found real things

The sentinel's audit found `rm -rf /` references (in safety rules documentation), private key references (in identity management code), and verified that all five safety checks pass. The reviewer found that the demo uses DID strings that look like hardcoded secrets (they're not — they're public identifiers). The researcher produced a quantitative analysis of the safety layer's code coverage. These aren't toy results.

## What's Next

The fleet is live. Four agents on the GitLawb node, each with their own identity, each capable of claiming and executing tasks. The runner polls every 30 seconds in loop mode. Artifacts accumulate in `memory/gitlawb-runner/`.

Next steps:

- **Wire the runner into Aeon's GitHub Actions** — run it as a cron job that dispatches fleet tasks
- **Connect the UCAN delegation chain** — operator mints scoped tokens to agents, agents present them when claiming tasks
- **Add the bridge** — `bridge-cli.mjs` sits in front of the node, verifying HTTP signatures and UCAN chains on every event
- **Trust score progression** — agents that complete tasks successfully get higher trust scores, unlocking longer TTLs
- **Swarm coordination** — `SwarmCoordinator.runParallel()` and `runHierarchical()` for multi-agent task decomposition

The infrastructure is built. The agents are registered. The task queue is flowing. The safety layer is hard at work.

```bash
# Run the fleet
node prototypes/gitlawb-safety/task-runner.mjs once

# Continuous polling
node prototypes/gitlawb-safety/task-runner.mjs loop --poll 30

# Dispatch a task
gl task create "research" \
  --assignee-did "did:key:z6MkfnrSD..." \
  --capability "issue:create" \
  --payload '{"topic":"your topic here"}'
```

---

*Built with the [GitLawb safety prototype](https://github.com/rsavitt/aeon/tree/codex/pr-review-multiline-var/prototypes/gitlawb-safety). Fleet identities at `~/.gitlawb/fleet/`. Runner at `prototypes/gitlawb-safety/task-runner.mjs`.*
