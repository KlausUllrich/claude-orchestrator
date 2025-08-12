#!/bin/bash
# Claude wrapper script with signaling

OUTPUT_FILE="$1"
SIGNAL_FILE="$2"
QUESTION="$3"

echo "[$(date +'%H:%M:%S')] Starting Claude query: $QUESTION" >&2

# Run claude and capture output
claude -p "$QUESTION" > "$OUTPUT_FILE" 2>&1

# Write completion signal
echo "{
  \"completed\": true,
  \"timestamp\": \"$(date -Iseconds)\",
  \"output_file\": \"$OUTPUT_FILE\"
}" > "$SIGNAL_FILE"

echo "[$(date +'%H:%M:%S')] Claude query completed, signal written to $SIGNAL_FILE" >&2
