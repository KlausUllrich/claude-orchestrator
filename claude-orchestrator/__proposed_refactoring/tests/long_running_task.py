#!/usr/bin/env python3
"""
A long-running task to test Claude's autonomy
"""
import time
from datetime import datetime

print(f"[{datetime.now().strftime('%H:%M:%S')}] SUBPROCESS: Starting 20-second task...")

for i in range(20):
    if i % 5 == 0:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] SUBPROCESS: Working... {i}/20 seconds")
    time.sleep(1)

print(f"[{datetime.now().strftime('%H:%M:%S')}] SUBPROCESS: Task complete!")

# Write completion marker
with open(".orchestrate/tests/subprocess_done.txt", "w") as f:
    f.write(f"Completed at {datetime.now()}")