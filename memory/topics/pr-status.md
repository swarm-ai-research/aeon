# PR Status

*Last updated: 2026-07-03*

Cross-repo PR queue for this aeon instance. Author: `aeonframework`, branch prefix: `ai/`, bot email: `aeonframework@users.noreply.github.com`. This run continues the inline OR filter per [[pr-tracker-branch-prefix-misses-bot-identity]] — accept if branch startswith `ai/` OR commit email matches the bot noreply — and widened it further to also accept the new `aeon@aeonframework.dev` domain (see today's Vibe-Trading#390 below).

## Open (3)

| Repo | PR | Title | Opened | Age | Activity |
|------|----|-------|--------|-----|----------|
| HKUDS/Vibe-Trading | [#390](https://github.com/HKUDS/Vibe-Trading/pull/390) | fix(deps): bump Pillow and langchain floors past disclosed CVEs | 2026-07-03 | 2h | fresh — 0 reviews / 0 comments |
| tamnd/kage | [#66](https://github.com/tamnd/kage/pull/66) | fix(deps): bump golang.org/x/image to v0.43.0 (3 advisories) | 2026-07-02 | 11h | fresh — 0 reviews / 0 comments |
| Panniantong/Agent-Reach | [#436](https://github.com/Panniantong/Agent-Reach/pull/436) | fix(deps): bump yt-dlp, requests, python-dotenv to patch disclosed CVEs | 2026-06-26 | 6d 15h | 0 reviews / 0 comments — crosses 7d at 19:24Z tonight |

## Recent Merges (last 30d)

| Repo | PR | Title | Opened | Merged |
|------|----|-------|--------|--------|
| _none_ | | | | |

## Closed No-Merge (last 30d)

| Repo | PR | Title | Closed | Notes |
|------|----|-------|--------|-------|
| _none_ | | | | |

---

GraphQL `author:aeonframework is:pr` → `issueCount: 3` (2026-07-03T10:20Z). Two **new** bot PRs opened in the last 24h — first non-Agent-Reach entries since 2026-06-26:

1. **HKUDS/Vibe-Trading#390** — opened 2026-07-03T08:14Z (2h ago), branch `security/bump-pillow-langchain-cves`, **commit author `aeon@aeonframework.dev` — new email**, not the `aeonframework@users.noreply.github.com` used by every prior bot PR. Same author account, same PR pattern (`fix(deps): bump …`), same `security/bump-*` branch convention. Accepted by widening the inline filter to include `@aeonframework.dev` for this run. **Suggests aeon has adopted a second commit-author identity.** Durable fix will need to widen `BOT_EMAIL` to a domain or list.
2. **tamnd/kage#66** — opened 2026-07-02T23:30Z (11h ago), branch `security/bump-x-image-0.43.0`, commit author `aeonframework@users.noreply.github.com` — matches the standard bot email.
3. **Panniantong/Agent-Reach#436** — opened 2026-06-26T19:24Z (**6d 15h old**, 0 activity, `updatedAt` unchanged). Predicted in MEMORY.md to cross the 7d stale threshold on today's run; my read is that the 10:00Z scheduled run **misses by ~9h** — the PR crosses at **2026-07-03T19:24Z tonight**, so **tomorrow's 10:00Z run will flag it stale** (assuming still unreviewed).

None of the three use the `ai/` branch prefix — the SKILL.md-documented `select(prefix) AND select(email)` primary filter would drop all three. The inline OR widening (branch prefix OR any known bot email) keeps them.

SKILL.md still uses `select(prefix) AND select(email)` per [[gh-search-prs-api-drift]] / [[pr-tracker-branch-prefix-misses-bot-identity]]. This run patched AND→OR inline for the 5th consecutive day AND added the new email domain to the accept-list; the durable fix (edit step 2's jq to OR the filters and accept a domain/list of bot emails) is still pending. Fallback path (`gh search prs`) still references `headRefName`/`mergedAt`/`--state merged`, all now `gh` CLI drift; only the GraphQL primary path actually works.

## Categorization (today = 2026-07-03, now = 10:20Z)

- **Recent merges (7d):** 0
- **Stale open (>7d, no activity 7d):** 0 — Agent-Reach#436 is 6d 15h, crosses threshold tonight 19:24Z
- **Active open:** 3 (Vibe-Trading#390 fresh, kage#66 fresh, Agent-Reach#436 borderline)
- **Closed no-merge (7d):** 0

Notification: **skipped** per step 5 (zero merges, zero stale, zero closed-no-merge). Two fresh bot PRs opened in the last 24h are not a notification trigger by the current step-5 rule — this is a SKILL design gap worth revisiting; new bot PRs are the operator's primary signal.
