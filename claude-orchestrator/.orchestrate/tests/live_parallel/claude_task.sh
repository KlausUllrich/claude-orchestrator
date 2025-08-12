#!/bin/bash
TASK_ID=$1
QUESTION=$2
OUTPUT_DIR=".orchestrate/tests/live_parallel/outputs"
STATUS_DIR=".orchestrate/tests/live_parallel/status"

mkdir -p "$OUTPUT_DIR" "$STATUS_DIR"

# Write starting status
echo '{"task":"'$TASK_ID'","state":"starting","timestamp":"'$(date -Iseconds)'"}' > "$STATUS_DIR/$TASK_ID.json"

echo "[$(date +'%H:%M:%S')] Task $TASK_ID starting: $QUESTION"

# Write running status
echo '{"task":"'$TASK_ID'","state":"running","timestamp":"'$(date -Iseconds)'"}' > "$STATUS_DIR/$TASK_ID.json"

# Run Claude and capture output
claude -p "$QUESTION" > "$OUTPUT_DIR/$TASK_ID.txt" 2>&1

# Write completed status with result location
echo '{"task":"'$TASK_ID'","state":"completed","timestamp":"'$(date -Iseconds)'","output":"'$OUTPUT_DIR/$TASK_ID.txt'"}' > "$STATUS_DIR/$TASK_ID.json"

echo "[$(date +'%H:%M:%S')] Task $TASK_ID completed!"