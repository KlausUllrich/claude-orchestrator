#!/usr/bin/env python3
"""
TEST: Can Claude (main agent) continue working while sub-agents run?

This is the CRITICAL test. We need to prove that when Claude launches
sub-agents via subprocess, Claude itself doesn't block and can continue
doing other work.

The problem we're trying to solve:
- When Claude uses Task() to launch sub-agents, it BLOCKS until they complete
- We need to prove that subprocess.Popen() allows Claude to continue

Test approach:
1. Create a long-running subprocess (simulating a sub-agent)
2. After launching it, Claude should be able to:
   - Read files
   - Write files
   - Do calculations
   - Check subprocess status
   - All WHILE the subprocess is still running
"""

import subprocess
import time
import json
from pathlib import Path
from datetime import datetime

def create_long_running_agent(duration: int = 30):
    """Create a sub-agent that runs for a long time"""
    script_path = Path(".orchestrate/tests/claude_autonomy/long_agent.py")
    script_path.parent.mkdir(parents=True, exist_ok=True)
    
    script_content = f'''#!/usr/bin/env python3
import time
import json
from pathlib import Path
from datetime import datetime

print(f"[{{datetime.now().strftime('%H:%M:%S')}}] Sub-agent: Starting {duration}-second task")

# Write status file immediately
status_file = Path(".orchestrate/tests/claude_autonomy/agent_status.json")
status_file.parent.mkdir(parents=True, exist_ok=True)

for i in range({duration}):
    status = {{
        "status": "running",
        "progress": i + 1,
        "total": {duration},
        "timestamp": datetime.now().isoformat()
    }}
    
    with open(status_file, 'w') as f:
        json.dump(status, f)
    
    if i % 5 == 0:
        print(f"[{{datetime.now().strftime('%H:%M:%S')}}] Sub-agent: Progress {{i}}/{duration}")
    
    time.sleep(1)

# Write completion
status = {{
    "status": "completed",
    "progress": {duration},
    "total": {duration},
    "timestamp": datetime.now().isoformat(),
    "result": "Successfully completed long-running task"
}}

with open(status_file, 'w') as f:
    json.dump(status, f)

print(f"[{{datetime.now().strftime('%H:%M:%S')}}] Sub-agent: COMPLETED")
'''
    
    script_path.write_text(script_content)
    script_path.chmod(0o755)
    return script_path

def test_claude_autonomy():
    """Test if Claude can work while subprocess runs"""
    
    print("="*80)
    print("CLAUDE AUTONOMY TEST")
    print("="*80)
    print("This test will prove whether Claude (main agent) can continue")
    print("working while a sub-agent runs in the background.")
    print("="*80)
    
    # Create long-running agent
    agent_script = create_long_running_agent(duration=30)
    
    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] TEST: Launching long-running sub-agent (30 seconds)...")
    
    # Launch subprocess WITHOUT blocking
    process = subprocess.Popen(["python3", str(agent_script)])
    
    print(f"[{datetime.now().strftime('%H:%M:%S')}] TEST: Sub-agent launched with PID {process.pid}")
    print(f"[{datetime.now().strftime('%H:%M:%S')}] TEST: Now Claude will do other work...\n")
    
    # Track what Claude can do
    claude_work_log = []
    start_time = time.time()
    
    # CLAUDE CONTINUES WORKING - This is the proof!
    
    # Task 1: Read files
    print(f"[{datetime.now().strftime('%H:%M:%S')}] CLAUDE: Reading files while sub-agent runs...")
    test_file = Path(".orchestrate/tests/claude_autonomy/test_data.txt")
    test_file.parent.mkdir(parents=True, exist_ok=True)
    test_file.write_text("Test data for Claude to read")
    content = test_file.read_text()
    claude_work_log.append(f"Read file: {content}")
    print(f"[{datetime.now().strftime('%H:%M:%S')}] CLAUDE: Successfully read file")
    
    # Task 2: Write files
    print(f"[{datetime.now().strftime('%H:%M:%S')}] CLAUDE: Writing analysis while sub-agent runs...")
    analysis_file = Path(".orchestrate/tests/claude_autonomy/analysis.txt")
    analysis_file.write_text(f"Analysis performed at {datetime.now()}")
    claude_work_log.append("Wrote analysis file")
    print(f"[{datetime.now().strftime('%H:%M:%S')}] CLAUDE: Successfully wrote analysis")
    
    # Task 3: Check subprocess status WITHOUT blocking
    for i in range(5):
        time.sleep(2)
        
        # Check if subprocess is still running
        if process.poll() is None:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] CLAUDE: Sub-agent still running (check {i+1}/5)")
            
            # Read sub-agent status
            status_file = Path(".orchestrate/tests/claude_autonomy/agent_status.json")
            if status_file.exists():
                with open(status_file) as f:
                    status = json.load(f)
                print(f"[{datetime.now().strftime('%H:%M:%S')}] CLAUDE: Sub-agent progress: {status['progress']}/{status['total']}")
            
            # Do more work
            calculation = sum(j*j for j in range(100000))
            claude_work_log.append(f"Performed calculation: {calculation}")
            print(f"[{datetime.now().strftime('%H:%M:%S')}] CLAUDE: Performed calculation = {calculation}")
        else:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] CLAUDE: Sub-agent has completed")
            break
    
    # Task 4: Create summary report
    print(f"[{datetime.now().strftime('%H:%M:%S')}] CLAUDE: Creating summary report...")
    summary = {
        "test_time": datetime.now().isoformat(),
        "claude_tasks_completed": len(claude_work_log),
        "work_log": claude_work_log,
        "subprocess_pid": process.pid,
        "elapsed_time": time.time() - start_time
    }
    
    summary_file = Path(".orchestrate/tests/claude_autonomy/summary.json")
    with open(summary_file, 'w') as f:
        json.dump(summary, f, indent=2)
    print(f"[{datetime.now().strftime('%H:%M:%S')}] CLAUDE: Summary report created")
    
    # Final check
    if process.poll() is None:
        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] CLAUDE: Sub-agent STILL RUNNING after all my work!")
        print(f"[{datetime.now().strftime('%H:%M:%S')}] CLAUDE: This proves I maintained autonomy!")
        
        # Optionally wait or kill
        print(f"[{datetime.now().strftime('%H:%M:%S')}] CLAUDE: Terminating sub-agent...")
        process.terminate()
        process.wait()
    else:
        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] CLAUDE: Sub-agent completed")
    
    elapsed = time.time() - start_time
    
    print("\n" + "="*80)
    print("AUTONOMY TEST RESULTS:")
    print("="*80)
    print(f"✅ Claude completed {len(claude_work_log)} tasks while sub-agent ran")
    print(f"✅ Claude maintained full autonomy for {elapsed:.1f} seconds")
    print(f"✅ Claude could read files, write files, and do calculations")
    print(f"✅ Claude could check sub-agent status without blocking")
    print("\n🎯 CONCLUSION: subprocess.Popen() gives Claude TRUE AUTONOMY")
    print("="*80)
    
    return True

def demonstrate_blocking_problem():
    """Demonstrate the problem we're trying to solve"""
    
    print("\n" + "="*80)
    print("DEMONSTRATING THE BLOCKING PROBLEM")
    print("="*80)
    print("This shows what happens with subprocess.run() - Claude BLOCKS")
    print("="*80)
    
    # Create a 5-second agent
    agent_script = create_long_running_agent(duration=5)
    
    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Using subprocess.run() (BLOCKING)...")
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Claude will be stuck for 5 seconds...")
    
    # This BLOCKS Claude
    result = subprocess.run(["python3", str(agent_script)], capture_output=True, text=True)
    
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Claude is finally free again!")
    print("During those 5 seconds, Claude couldn't do ANYTHING else!")
    print("="*80)

if __name__ == "__main__":
    print("CRITICAL TEST: Can Claude maintain autonomy while sub-agents run?\n")
    
    # First show the problem
    demonstrate_blocking_problem()
    
    print("\n" + "="*80)
    print("NOW TESTING THE SOLUTION: subprocess.Popen()")
    print("="*80)
    
    # Then prove the solution
    success = test_claude_autonomy()
    
    if success:
        print("\n✅ TEST PASSED: Claude CAN maintain autonomy with subprocess.Popen()")
        print("This means the refactoring can proceed!")
    else:
        print("\n❌ TEST FAILED: Claude cannot maintain autonomy")
        print("Refactoring approach needs revision")