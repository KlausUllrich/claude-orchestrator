#!/usr/bin/env python3
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
    print(f"\r[{datetime.now().strftime('%H:%M:%S')}] Waiting for Claude{'.' * (dots % 4)}    ", end="", flush=True)
    
    dots += 1
    time.sleep(1)

# Signal received!
print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Signal received! Claude has completed.")

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
