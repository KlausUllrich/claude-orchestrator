#!/bin/bash
# Launch script for Claude background test

BASE_DIR=".orchestrate/tests/claude_background"
OUTPUT_FILE="$BASE_DIR/outputs/claude_response.txt"
SIGNAL_FILE="$BASE_DIR/signals/claude.signal"
QUESTION="what is the greatest leader in history"

echo "=========================================="
echo "Claude Background Test with File Signaling"
echo "=========================================="
echo ""
echo "This test will:"
echo "1. Launch Claude in background to answer: '$QUESTION'"
echo "2. Run a parallel worker doing other tasks"
echo "3. Monitor for completion signal"
echo "4. Show Claude's response when ready"
echo ""
echo "Starting in 3 seconds..."
sleep 3

# Clean previous runs
rm -f "$SIGNAL_FILE" "$OUTPUT_FILE"

echo "[$(date +'%H:%M:%S')] Launching Claude in background..."
bash ".orchestrate/tests/claude_background/claude_wrapper.sh" "$OUTPUT_FILE" "$SIGNAL_FILE" "$QUESTION" &
CLAUDE_PID=$!

echo "[$(date +'%H:%M:%S')] Launching parallel worker..."
python ".orchestrate/tests/claude_background/parallel_worker.py" &
WORKER_PID=$!

echo "[$(date +'%H:%M:%S')] Starting monitor..."
python ".orchestrate/tests/claude_background/progress_monitor.py" "$SIGNAL_FILE"

# Wait for worker to complete
wait $WORKER_PID 2>/dev/null

echo ""
echo "=========================================="
echo "Test Results:"
echo "=========================================="
echo ""
echo "Claude's Response:"
echo "------------------"
cat "$OUTPUT_FILE" 2>/dev/null || echo "No response file found"
echo ""
echo "------------------"
echo ""
echo "Work completed while waiting:"
if [ -f "$BASE_DIR/work_log.json" ]; then
    python -c "import json; d=json.load(open('$BASE_DIR/work_log.json')); print(f'Processed {len(d[\"completed_items\"])} items')"
fi
echo ""
echo "Test completed!"
