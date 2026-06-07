---
name: Note Taking
description: Save a note as one or more atomic notes under memory/notes/ (and optionally Supernotes). Splits bundled inputs into separate atomic files.
var: ""
tags: [meta]
---
> **${var}** — The note content to save. Can be a thought, idea, link, quote, or anything worth remembering.

Read `memory/MEMORY.md` for context.

## Destinations

This skill writes to two destinations:

1. **Atomic files under `memory/notes/${slug}.md`** (always) — one file per claim. These become nodes in `notegraph.json` and are linkable via `[[slug]]` from MOCs (`memory/topics/*.md`) and other notes.
2. **Supernotes** (if `SUPERNOTES_API_KEY` is set) — queues a card per atomic note via the post-process pattern.

A daily index at `memory/notes/daily/${today}.md` collects `[[slug]]` pointers to every note saved that day, so you can still browse by date.

## Atomicity gate (the core change vs prior versions)

A note is **atomic** if its title states a single claim and the body can be summarized in ≤3 coherent sentences without "and also" / "additionally" / "moreover".

Bundled inputs become "linking hazards" — you want to reference one claim, drag unrelated ones along — and weaken the graph because `[[X]]` ends up pointing at a topic dump instead of one idea. So this skill **splits before saving**.

## Steps

1. **Parse the input.** `${var}` is the note. If empty, check `memory/logs/${today}.md` for the most recent notable finding and use that. If neither yields content, log `NOTE_TAKING_SKIP: no input` and stop.

2. **Atomicity check + split.** Read the input and count the distinct claims it makes.
   - **1 claim** → continue as a single note (one save).
   - **2+ claims** → split into N notes. Each claim gets its own title, body, slug, frontmatter, and file. Cross-link them: every split note's `links:` frontmatter includes the slugs of its siblings.
   - **Heuristics for "claim count":**
     - The input describes N distinct facts/events/decisions joined by "and", "also", semicolons, or paragraph breaks.
     - The input mentions ≥2 unrelated entities (people, repos, PRs, skills) each with its own action.
     - You'd write more than 3 sentences to summarize without losing information.
   - **When in doubt, split.** A note that turns out to be one claim with rich detail is fine; a bundled note is permanently a linking hazard. Splitting is cheap, merging later is fine too.

3. **For each atomic note**, run steps 4–9 below.

4. **Clean up the note.** Keep the user's intent and voice intact — don't rewrite, just tidy. If the source is a URL, WebFetch it and include a one-line summary as context. Raw thoughts stay raw.

5. **Generate a slug** — kebab-case, 2–5 words, derived from the title. Must be unique under `memory/notes/`. If a file with that slug already exists, append a disambiguator (`-2026-06-06` or a topic suffix).

6. **Generate a title** — short, descriptive H1 stating the single claim. 3–8 words.

7. **Pick a color** (Supernotes only, ignored locally):
   - `blue` — information, links, references
   - `green` — ideas, plans, things to build
   - `yellow` — questions, things to investigate
   - `red` — urgent, time-sensitive
   - `purple` — opinions, takes, hot thoughts

8. **Pick 1–3 tags** (lowercase, hyphenated). Always include `aeon`.

9. **Write the atomic file** at `memory/notes/${slug}.md`:

   ```markdown
   ---
   id: ${slug}
   created: ${today}
   type: ${type}    # claim | thesis | artifact | incident | lesson | observation | question | status
   links: ${SIBLING_SLUGS_IF_SPLIT}
   ---
   # ${TITLE}

   ${BODY}
   ```

   ```bash
   mkdir -p memory/notes
   cat > "memory/notes/${SLUG}.md" <<EOF
   ---
   id: ${SLUG}
   created: ${TODAY}
   type: ${TYPE}
   links: ${LINKS}
   ---
   # ${TITLE}

   ${BODY}
   EOF
   ```

   **Self-check after write:** read the file back and confirm the body is ≤3 sentences excluding the title line. If it's longer, you bundled — delete the file and re-split.

10. **Update the daily index** at `memory/notes/daily/${today}.md` — append a pointer line per saved note:

    ```bash
    mkdir -p memory/notes/daily
    if [ ! -f "memory/notes/daily/${TODAY}.md" ]; then
      echo "# Notes — ${TODAY}" > "memory/notes/daily/${TODAY}.md"
      echo "" >> "memory/notes/daily/${TODAY}.md"
    fi
    echo "- [[${SLUG}]] — ${TITLE} *(${HH}:${MM} UTC, tags: ${TAGS}, color: ${COLOR})*" \
      >> "memory/notes/daily/${TODAY}.md"
    ```

11. **Supernotes (if configured)** — write one request file per atomic note (sandbox blocks direct curl; workflow post-processes):

    ```bash
    if [ -n "$SUPERNOTES_API_KEY" ]; then
      mkdir -p .pending-supernotes
      jq -n \
        --arg name "$TITLE" \
        --arg markup "$MARKUP" \
        --arg color "$COLOR" \
        --argjson tags "$(printf '%s\n' "${TAGS_ARRAY[@]}" | jq -R . | jq -s .)" \
        '{name: $name, markup: $markup, color: $color, tags: $tags}' \
        > ".pending-supernotes/note-$(date -u +%s)-${SLUG}.json"
    fi
    ```

12. **Confirmation via `./notify`** — one line per save run, summarizing the split:
    ```
    note saved: ${N} atomic note(s) — ${FIRST_TITLE}${ETC}
    ```
    Keep it short. If N>1, append `(split from bundled input)` so the operator sees the gate fired. If Supernotes was skipped, optionally append `(local only — set SUPERNOTES_API_KEY for sync)` on the first run per day; suppress that hint afterwards.

13. **Log to `memory/logs/${today}.md`:**

    ```markdown
    ## Note Taking
    - **Saved:** ${N} atomic note(s)
    - **Slugs:** [[slug-1]], [[slug-2]], …
    - **Split:** yes / no (gate fired if N>1 from a single input)
    - **Supernotes:** queued (${N} cards) / skipped (no key)
    - NOTE_TAKING_OK
    ```

## Examples

### Atomic input (no split)

> "Surplus Intelligence x402 endpoint is real but no paid call yet — needs funded Base wallet."

Single claim. One file: `memory/notes/surplus-x402-real-endpoint.md`. Title: "SURPLUS_X402 is a real x402 inference endpoint". Body: ≤3 sentences. Daily index gets one pointer.

### Bundled input (gate fires)

> "PR #107 merged 2026-06-02 fixing the vuln-scanner allowlist and the rss-feed allowlist and the heartbeat eval timing gap, plus we moved skill-evals from 06:00 to 09:00 UTC."

Four distinct claims joined by "and". Gate splits into four notes:
- `pr-107-merged.md` — the PR ship event
- `vuln-scanner-allowlist-fix.md` — the ISS-004 fix
- `rss-feed-allowlist-fix.md` — the ISS-005 fix
- `skill-evals-09utc-move.md` — the schedule change

Each note's `links:` lists the other three. Daily index gets four pointers. Notify: `note saved: 4 atomic notes — PR #107 merged… (split from bundled input)`.

## Environment Variables

- `SUPERNOTES_API_KEY` — optional. When set, each atomic note is also queued for Supernotes.

## Sandbox Note

- Direct calls to Supernotes' API are blocked by the GitHub Actions sandbox; the skill writes one JSON payload per note to `.pending-supernotes/` and a post-process step delivers them after Claude finishes.
- Local file writes happen inside the sandbox without issue.
- WebFetch for URL summaries bypasses the sandbox.

## Why this matters

Atomic notes are the structural requirement for `notegraph.json` to compound. A bundled note becomes a "linking hazard" — `[[X]]` ends up pointing at a topic dump instead of a single claim. Atomic notes make links precise, let backlinks implicitly define a concept by the contexts that invoked it, and make multi-hop traversal reliable. See the pilot in PR #260 for the validated effect: edges grew 5.3× faster than nodes across three topic atomizations.
