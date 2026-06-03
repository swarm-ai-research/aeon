#!/usr/bin/env bash
# Pre-fetch live Surplus Intelligence model prices OUTSIDE the Claude sandbox.
#
# The GitHub Actions sandbox blocks outbound fetch from INSIDE the sim, so the
# workflow fetches the live Surplus feed here (full network access) and caches
# it to .surplus-cache/prices.json. The compute-futures sim run with
# `--surplus --live` reads that cache via readCachedSurplusPrices() in
# prototypes/compute-futures/src/surplus.mjs — no in-sandbox network call.
#
# Configure SURPLUS_PRICING_URL (repo secret/var) to a Surplus prices or
# OpenAI-compatible /models endpoint returning either
#   { "models": { "<id>": { "input": <num>, "output": <num> } } }
# or an OpenAI-style list ([{ "id": "...", "input": ..., "output": ... }]).
# Optionally set SURPLUS_API_KEY for a Bearer header.
#
# If SURPLUS_PRICING_URL is unset or the fetch fails, this no-ops and the sim
# falls back to its built-in catalog (deterministic) — never fatal.
set -euo pipefail

SKILL="${1:-}"
VAR="${2:-}"

# Only relevant to the Surplus consumers; skip otherwise to avoid noise.
case "$SKILL" in
  surplus-pulse | compute-futures*) ;;
  *) exit 0 ;;
esac

if [ -z "${SURPLUS_PRICING_URL:-}" ]; then
  echo "prefetch-surplus: SURPLUS_PRICING_URL not set, skipping (sim will use catalog)"
  exit 0
fi

mkdir -p .surplus-cache
OUT=".surplus-cache/prices.json"

attempt=1
max=4
while [ "$attempt" -le "$max" ]; do
  echo "prefetch-surplus: fetching live prices (attempt $attempt/$max) ..."
  http_code=$(curl -sS -m 20 -H "accept: application/json" \
    ${SURPLUS_API_KEY:+-H "authorization: Bearer $SURPLUS_API_KEY"} \
    -o "$OUT.tmp" -w "%{http_code}" "$SURPLUS_PRICING_URL" 2>/dev/null || echo "000")
  if [ "$http_code" = "200" ] && jq -e . "$OUT.tmp" >/dev/null 2>&1; then
    mv "$OUT.tmp" "$OUT"
    echo "prefetch-surplus: cached live prices to $OUT (HTTP 200)"
    exit 0
  fi
  echo "prefetch-surplus: attempt $attempt failed (HTTP $http_code)"
  rm -f "$OUT.tmp"
  attempt=$((attempt + 1))
  [ "$attempt" -le "$max" ] && sleep $((2 ** (attempt - 1)))
done

echo "prefetch-surplus: all attempts failed — sim will fall back to catalog"
exit 0
