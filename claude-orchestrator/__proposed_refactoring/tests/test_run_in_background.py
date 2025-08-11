#!/usr/bin/env python3
"""
Test #1: run_in_background parameter
Testing Claude's ability to maintain autonomy using the run_in_background parameter
"""

import time
from datetime import datetime
from pathlib import Path

def create_test_script(name: str, duration: int, output_interval: int = 2):
    """Create a test script that runs for specified duration"""
    script_path = Path(f".orchestrate/tests/background/{name}.py")
    script_path.parent.mkdir(parents=True, exist_ok=True)
    
    script_content = f'''#!/usr/bin/env python3
import time
from datetime import datetime
from pathlib import Path

print(f"[{{datetime.now().strftime('%H:%M:%S.%f')[:-3]}}] {name}: STARTED (will run for {duration}s)")

status_file = Path(".orchestrate/tests/background/{name}_status.txt")
status_file.parent.mkdir(parents=True, exist_ok=True)

for i in range({duration}):
    if i % {output_interval} == 0:
        print(f"[{{datetime.now().strftime('%H:%M:%S.%f')[:-3]}}] {name}: Progress {{i}}/{duration}s")
        
        # Write status to file
        with open(status_file, 'w') as f:
            f.write(f"{{i}}/{duration} seconds completed at {{datetime.now()}}")
    
    time.sleep(1)

print(f"[{{datetime.now().strftime('%H:%M:%S.%f')[:-3]}}] {name}: COMPLETED")

# Write completion marker
with open(status_file, 'w') as f:
    f.write(f"COMPLETED at {{datetime.now()}}")
'''
    
    script_path.write_text(script_content)
    script_path.chmod(0o755)
    return script_path

# Create test scripts with different durations
print("Creating test scripts...")
script1 = create_test_script("Agent_A", 20, 3)
script2 = create_test_script("Agent_B", 15, 3)
script3 = create_test_script("Agent_C", 10, 2)

print(f"Created scripts:")
print(f"  - {script1} (20s duration)")
print(f"  - {script2} (15s duration)")
print(f"  - {script3} (10s duration)")

print("\nTest scripts ready for Claude to execute with run_in_background parameter")
print("Claude should:")
print("1. Launch each script with run_in_background=True")
print("2. Continue working while scripts run")
print("3. Check status using BashOutput tool")
print("4. Read status files to monitor progress")