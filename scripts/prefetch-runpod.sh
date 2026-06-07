#!/usr/bin/env bash
# Pre-fetch RunPod GraphQL GPU pricing OUTSIDE the Claude sandbox.
# Skill reads cached JSON from .runpod-cache/gpu-types.json
set -euo pipefail

SKILL="${1:-}"

if [ -z "$SKILL" ]; then
  echo "Usage: prefetch-runpod.sh <skill-name>"
  exit 1
fi

# Only run for skills that need RunPod pricing.
case "$SKILL" in
  runpod-spot-pricing) ;;
  *)
    echo "runpod-prefetch: no prefetch defined for skill '$SKILL'"
    exit 0
    ;;
esac

if [ -z "${RUNPOD_API_KEY:-}" ]; then
  echo "runpod-prefetch: RUNPOD_API_KEY not set, skipping"
  exit 0
fi

mkdir -p .runpod-cache

# Codex review on PR #118: a single unfiltered `lowestPrice(input:{gpuCount:1})`
# call returns the cheapest across BOTH pools, so for GPUs available in both
# secure and community cloud the skill ended up comparing minimumBidPrice from
# one pool against uninterruptablePrice from the other, producing false >50%
# discount signals. Query each pool separately via GraphQL aliases so the
# downstream comparison is like-for-like.
# Ref: https://docs.runpod.io/sdks/graphql/manage-pods#check-gpu-availability
QUERY='{"query":"query GpuTypes { gpuTypes { id displayName memoryInGb secureCloud communityCloud secure: lowestPrice(input:{gpuCount:1, secureCloud:true}) { minimumBidPrice uninterruptablePrice } community: lowestPrice(input:{gpuCount:1, secureCloud:false}) { minimumBidPrice uninterruptablePrice } } }"}'

echo "runpod-prefetch: querying gpuTypes ..."
response=$(curl -s --max-time 60 -w "\n__HTTP_CODE__%{http_code}" \
  -X POST "https://api.runpod.io/graphql" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $RUNPOD_API_KEY" \
  -d "$QUERY" 2>&1) || {
    echo "::warning::runpod-prefetch: curl failed"
    exit 0
  }

http_code=$(echo "$response" | grep '__HTTP_CODE__' | sed 's/__HTTP_CODE__//')
body=$(echo "$response" | grep -v '__HTTP_CODE__')

if [ "$http_code" != "200" ]; then
  echo "::warning::runpod-prefetch: HTTP $http_code"
  echo "::warning::runpod-prefetch: response: $(echo "$body" | head -c 300)"
  exit 0
fi

if ! echo "$body" | jq -e '.data.gpuTypes | length > 0' >/dev/null 2>&1; then
  echo "::warning::runpod-prefetch: response had no gpuTypes array"
  echo "::warning::runpod-prefetch: response: $(echo "$body" | head -c 300)"
  exit 0
fi

echo "$body" > .runpod-cache/gpu-types.json
COUNT=$(echo "$body" | jq '.data.gpuTypes | length')
echo "runpod-prefetch: saved gpu-types.json ($COUNT GPU types)"
