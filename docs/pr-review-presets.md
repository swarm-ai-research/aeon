# PR Review Presets for `pr-review`

These presets are ready to paste into `aeon.yml` under the `pr-review` skill `var` field.

## Merge Gate (strict)

```yaml
skills:
  pr-review:
    enabled: true
    schedule: "0 */6 * * *"
    var: |
      swarm-ai-research/swarm

      You are acting as a merge gate reviewer.
      Your job is to decide: APPROVE, REQUEST_CHANGES, or BLOCK.

      Decision policy:
      - BLOCK if any critical security/correctness risk is present.
      - REQUEST_CHANGES if important test coverage or reliability safeguards are missing.
      - APPROVE only if risk is low and evidence is sufficient.
```

## Fast Lane (low-risk)

```yaml
skills:
  pr-review:
    enabled: true
    schedule: "0 */6 * * *"
    var: |
      swarm-ai-research/swarm

      You are a fast-lane PR reviewer.
      Goal: quickly approve genuinely low-risk changes while still catching real hazards.

      Fast-lane eligibility:
      - Docs/comments/formatting-only changes.
      - Small refactors with no behavior change.
      - No sensitive auth/security/runtime interfaces touched.
```

## Auto Router (recommended)

```yaml
skills:
  pr-review:
    enabled: true
    schedule: "0 */6 * * *"
    var: |
      swarm-ai-research/swarm

      You are an auto-routing PR reviewer and merge gate.

      Step 1: Classify PR risk first
      Assign one: LOW | MEDIUM | HIGH based on files touched and behavior risk.

      Routing policy:
      - LOW -> FAST_LANE
      - MEDIUM or HIGH -> STRICT_GATE

      Output format:
      # PR Review Router Decision
      Risk Tier: LOW | MEDIUM | HIGH
      Routed Mode: FAST_LANE | STRICT_GATE
      Final Decision: APPROVE_FAST | ESCALATE_FULL_REVIEW | REQUEST_CHANGES | APPROVE | BLOCK
```

## Notes

- Use `var: "owner/repo"` to scope dev/code skills to a target repository.
- Keep `heartbeat` last in `aeon.yml` because skill ordering affects scheduler selection.
