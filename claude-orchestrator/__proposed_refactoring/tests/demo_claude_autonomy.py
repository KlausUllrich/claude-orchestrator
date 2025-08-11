#!/usr/bin/env python3
"""
Demonstration script for Claude to run
This will launch a subprocess and show Claude can continue
"""

import subprocess
import time
from datetime import datetime
from pathlib import Path

print("="*80)
print("CLAUDE AUTONOMY DEMONSTRATION")
print("="*80)

# Create a long-running script
long_script = Path(".orchestrate/tests/demo_long_task.py")
long_script.parent.mkdir(parents=True, exist_ok=True)

script_content = '''#!/usr/bin/env python3
import time
from datetime import datetime

print(f"[{datetime.now().strftime('%H:%M:%S')}] SUB-AGENT: Starting 15-second task")

for i in range(15):
    if i % 3 == 0:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] SUB-AGENT: Progress {i}/15")
    time.sleep(1)

print(f"[{datetime.now().strftime('%H:%M:%S')}] SUB-AGENT: Complete!")
'''

long_script.write_text(script_content)
long_script.chmod(0o755)

print(f"[{datetime.now().strftime('%H:%M:%S')}] CLAUDE: Launching subprocess with Popen...")

# Launch WITHOUT blocking
process = subprocess.Popen(["python3", str(long_script)])

print(f"[{datetime.now().strftime('%H:%M:%S')}] CLAUDE: Subprocess launched (PID: {process.pid})")
print(f"[{datetime.now().strftime('%H:%M:%S')}] CLAUDE: Now I'll continue working...\n")

# Claude continues working
for i in range(5):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] CLAUDE: Doing work iteration {i+1}")
    
    # Check subprocess status without blocking
    if process.poll() is None:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] CLAUDE: Subprocess still running")
    else:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] CLAUDE: Subprocess finished")
    
    time.sleep(2)

print(f"\n[{datetime.now().strftime('%H:%M:%S')}] CLAUDE: Finished my work!")

# Final status
if process.poll() is None:
    print(f"[{datetime.now().strftime('%H:%M:%S')}] CLAUDE: Subprocess STILL RUNNING - I maintained autonomy!")
    print(f"[{datetime.now().strftime('%H:%M:%S')}] CLAUDE: Waiting for subprocess to complete...")
    process.wait()
    
print("\n" + "="*80)
print("DEMONSTRATION COMPLETE")
print("Claude maintained full autonomy while subprocess ran!")
print("="*80)