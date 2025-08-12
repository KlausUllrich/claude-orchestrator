#!/usr/bin/env python3
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
