#!/usr/bin/env bash
# Post-process Replicate API requests left by Claude (sandbox blocks outbound curl).
# Reads .pending-replicate/*.json, makes the API call, downloads the image.
set -euo pipefail

PENDING_DIR=".pending-replicate"

if [ ! -d "$PENDING_DIR" ] || [ -z "$(ls -A "$PENDING_DIR"/*.json 2>/dev/null)" ]; then
  echo "replicate-postprocess: no pending requests"
  exit 0
fi

if [ -z "${REPLICATE_API_TOKEN:-}" ]; then
  echo "replicate-postprocess: REPLICATE_API_TOKEN not set, skipping"
  exit 0
fi

replicate_post() {
  local payload="$1" model="$2"
  curl -sf --max-time 60 -X POST \
    -H "Authorization: Bearer $REPLICATE_API_TOKEN" \
    -H "Content-Type: application/json" \
    -H "Prefer: wait" \
    -d "$payload" \
    "https://api.replicate.com/v1/models/${model}/predictions" 2>&1
}

for req_file in "$PENDING_DIR"/*.json; do
  [ -f "$req_file" ] || continue
  echo "replicate-postprocess: processing $(basename "$req_file")..."

  PROMPT=$(jq -r '.prompt // empty' "$req_file")
  ASPECT=$(jq -r '.aspect_ratio // "16:9"' "$req_file")
  OUTPUT_PATH=$(jq -r '.output_path // empty' "$req_file")
  MODEL=$(jq -r '.model // "google/nano-banana-pro"' "$req_file")

  if [ -z "$PROMPT" ] || [ -z "$OUTPUT_PATH" ]; then
    echo "replicate-postprocess: invalid request (missing prompt or output_path), skipping"
    continue
  fi

  BASE_PAYLOAD=$(jq -n \
    --arg prompt "$PROMPT" \
    --arg aspect "$ASPECT" \
    '{input: {prompt: $prompt, aspect_ratio: $aspect, number_of_images: 1, safety_tolerance: 5}}')

  # Create the prediction
  RESPONSE=$(replicate_post "$BASE_PAYLOAD" "$MODEL") || {
    echo "replicate-postprocess: API call failed for $(basename "$req_file")"

    # Retry with fallback model
    echo "replicate-postprocess: retrying with allow_fallback_model..."
    RESPONSE=$(replicate_post "$(echo "$BASE_PAYLOAD" | jq '.input.allow_fallback_model = true')" "$MODEL") || {
      echo "replicate-postprocess: retry also failed, skipping"
      continue
    }
  }

  # Extract image URL from response
  IMAGE_URL=$(echo "$RESPONSE" | jq -r '.output // empty | if type == "array" then .[0] else . end // empty')

  if [ -z "$IMAGE_URL" ]; then
    # Check if prediction is still processing (no "Prefer: wait" support)
    PRED_URL=$(echo "$RESPONSE" | jq -r '.urls.get // empty')
    if [ -n "$PRED_URL" ]; then
      echo "replicate-postprocess: polling for result..."
      for i in $(seq 1 12); do
        sleep 5
        POLL=$(curl -sf -H "Authorization: Bearer $REPLICATE_API_TOKEN" "$PRED_URL" 2>&1) || continue
        STATUS=$(echo "$POLL" | jq -r '.status // empty')
        if [ "$STATUS" = "succeeded" ]; then
          IMAGE_URL=$(echo "$POLL" | jq -r '.output // empty | if type == "array" then .[0] else . end // empty')
          break
        elif [ "$STATUS" = "failed" ] || [ "$STATUS" = "canceled" ]; then
          echo "replicate-postprocess: prediction $STATUS"
          break
        fi
      done
    fi
  fi

  if [ -z "$IMAGE_URL" ]; then
    echo "replicate-postprocess: no image URL in response, skipping"
    continue
  fi

  # Download the image
  mkdir -p "$(dirname "$OUTPUT_PATH")"
  if curl -sfL --max-time 30 "$IMAGE_URL" -o "$OUTPUT_PATH"; then
    echo "replicate-postprocess: saved $OUTPUT_PATH ($(wc -c < "$OUTPUT_PATH") bytes)"
    # Write a marker so Claude's skill output can reference the path
    echo "$OUTPUT_PATH" > "$PENDING_DIR/$(basename "$req_file" .json).done"
  else
    echo "replicate-postprocess: failed to download image from $IMAGE_URL"
  fi
done

echo "replicate-postprocess: done"
