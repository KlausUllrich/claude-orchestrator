#!/usr/bin/env python3
"""
Test File-Signaling with Claude CLI Background Process

This test demonstrates:
1. Launching claude CLI in background to answer a question
2. Main Claude continues working while background Claude processes
3. File-based signaling when background Claude completes
4. Reading the response from a file
"""

import json
import sys
import time
from pathlib import Path
from datetime import datetime

class ClaudeBackgroundTest:
    def __init__(self):
        self.base_dir = Path('.orchestrate/tests/claude_background')
        self.signal_dir = self.base_dir / 'signals'
        self.output_dir = self.base_dir / 'outputs'
        
        # Create directories
        self.signal_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def create_monitor_script(self):
        """Create a wrapper script that signals completion"""
        wrapper_script = self.base_dir / 'claude_wrapper.sh'
        
        script_content = '''#!/bin/bash
# Claude wrapper script with signaling

OUTPUT_FILE="$1"
SIGNAL_FILE="$2"
QUESTION="$3"

echo "[$(date +'%H:%M:%S')] Starting Claude query: $QUESTION" >&2

# Run claude and capture output
claude -p "$QUESTION" > "$OUTPUT_FILE" 2>&1

# Write completion signal
echo "{
  \\"completed\\": true,
  \\"timestamp\\": \\"$(date -Iseconds)\\",
  \\"output_file\\": \\"$OUTPUT_FILE\\"
}" > "$SIGNAL_FILE"

echo "[$(date +'%H:%M:%S')] Claude query completed, signal written to $SIGNAL_FILE" >&2
'''
        
        wrapper_script.write_text(script_content)
        wrapper_script.chmod(0o755)
        return wrapper_script
        
    def create_progress_monitor(self):
        """Create a script that shows progress while waiting"""
        monitor_script = self.base_dir / 'progress_monitor.py'
        
        script_content = '''#!/usr/bin/env python3
import time
import json
from pathlib import Path
from datetime import datetime

signal_file = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".orchestrate/tests/claude_background/signals/claude.signal")
status_file = Path(".orchestrate/tests/claude_background/status.json")

print(f"[{datetime.now().strftime('%H:%M:%S')}] Monitoring for Claude completion...")
print(f"Signal file: {signal_file}")

dots = 0
while not signal_file.exists():
    # Update status
    status = {
        "state": "waiting",
        "message": f"Waiting for Claude{'.' * (dots % 4)}",
        "timestamp": datetime.now().isoformat(),
        "elapsed_seconds": dots
    }
    status_file.write_text(json.dumps(status, indent=2))
    
    # Visual progress
    print(f"\\r[{datetime.now().strftime('%H:%M:%S')}] Waiting for Claude{'.' * (dots % 4)}    ", end="", flush=True)
    
    dots += 1
    time.sleep(1)

# Signal received!
print(f"\\n[{datetime.now().strftime('%H:%M:%S')}] Signal received! Claude has completed.")

# Read the signal
signal_data = json.loads(signal_file.read_text())
print(f"Output saved to: {signal_data['output_file']}")

# Final status
status = {
    "state": "completed",
    "message": "Claude query completed",
    "timestamp": datetime.now().isoformat(),
    "output_file": signal_data['output_file']
}
status_file.write_text(json.dumps(status, indent=2))
'''
        
        monitor_script.write_text(script_content.replace('import sys', 'import sys'))
        monitor_script.chmod(0o755)
        return monitor_script

    def create_parallel_worker(self):
        """Create a worker that does something while Claude runs"""
        worker_script = self.base_dir / 'parallel_worker.py'
        
        script_content = '''#!/usr/bin/env python3
import time
import json
from pathlib import Path
from datetime import datetime

print(f"[{datetime.now().strftime('%H:%M:%S')}] Parallel worker starting...")

work_log = Path(".orchestrate/tests/claude_background/work_log.json")
work_items = []

# Simulate doing work while Claude processes
for i in range(20):
    work_item = {
        "item": i + 1,
        "timestamp": datetime.now().isoformat(),
        "task": f"Processing item {i + 1}",
        "result": f"Item {i + 1} completed"
    }
    work_items.append(work_item)
    
    # Write progress
    work_log.write_text(json.dumps({
        "completed_items": work_items,
        "current_item": i + 1,
        "total_items": 20,
        "timestamp": datetime.now().isoformat()
    }, indent=2))
    
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Processed item {i + 1}/20")
    time.sleep(0.5)

print(f"[{datetime.now().strftime('%H:%M:%S')}] Parallel worker completed!")
'''
        
        worker_script.write_text(script_content)
        worker_script.chmod(0o755)
        return worker_script

    def setup_test(self):
        """Set up all test components"""
        print("Setting up Claude background test...")
        
        # Create scripts
        wrapper = self.create_monitor_script()
        monitor = self.create_progress_monitor()
        worker = self.create_parallel_worker()
        
        # Create launch script
        launch_script = self.base_dir / 'launch_test.sh'
        
        launch_content = f'''#!/bin/bash
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
bash "{wrapper}" "$OUTPUT_FILE" "$SIGNAL_FILE" "$QUESTION" &
CLAUDE_PID=$!

echo "[$(date +'%H:%M:%S')] Launching parallel worker..."
python "{worker}" &
WORKER_PID=$!

echo "[$(date +'%H:%M:%S')] Starting monitor..."
python "{monitor}" "$SIGNAL_FILE"

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
    python -c "import json; d=json.load(open('$BASE_DIR/work_log.json')); print(f'Processed {{len(d[\\"completed_items\\"])}} items')"
fi
echo ""
echo "Test completed!"
'''
        
        launch_script.write_text(launch_content)
        launch_script.chmod(0o755)
        
        print(f"Test setup complete!")
        print(f"Scripts created in: {self.base_dir}")
        print(f"")
        print(f"To run the test:")
        print(f"  bash {launch_script}")
        
        return launch_script

def main():
    test = ClaudeBackgroundTest()
    launch_script = test.setup_test()
    
    print("")
    print("Test can demonstrate:")
    print("- Claude running in background via CLI")
    print("- File-based completion signaling")
    print("- Parallel work while Claude processes")
    print("- Autonomous operation (main Claude not blocked)")
    
    return str(launch_script)

if __name__ == "__main__":
    script_path = main()
    print(f"\nLaunch script: {script_path}")