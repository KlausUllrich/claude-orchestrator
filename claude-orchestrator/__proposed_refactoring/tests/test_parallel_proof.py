#!/usr/bin/env python3
"""
DEFINITIVE PROOF OF PARALLEL EXECUTION
This test will show unmistakable evidence of parallel work
"""

import subprocess
import time
import threading
from pathlib import Path
from datetime import datetime
import sys

def create_worker_script(worker_id: str, task_type: str, duration: int):
    """Create a worker that does visible work"""
    script_path = Path(f".orchestrate/tests/parallel_proof/worker_{worker_id}.py")
    script_path.parent.mkdir(parents=True, exist_ok=True)
    
    script_content = f'''#!/usr/bin/env python3
import time
import sys
from datetime import datetime

worker_id = "{worker_id}"
task_type = "{task_type}"
duration = {duration}

# Force unbuffered output
sys.stdout = sys.stderr

def timestamp():
    return datetime.now().strftime("%H:%M:%S.%f")[:-3]

print(f"[{{timestamp()}}] {worker_id}: Starting {{task_type}} for {{duration}}s")

for i in range(duration):
    # Do actual work
    if task_type == "CALCULATION":
        result = sum(j*j for j in range(100000))
        print(f"[{{timestamp()}}] {worker_id}: Calculated sum of squares = {{result}}")
    elif task_type == "FILE_ANALYSIS":
        print(f"[{{timestamp()}}] {worker_id}: Analyzing file chunk {{i+1}}/{{duration}}")
    elif task_type == "API_CALLS":
        print(f"[{{timestamp()}}] {worker_id}: Making API request {{i+1}}/{{duration}}")
    elif task_type == "DATA_PROCESSING":
        print(f"[{{timestamp()}}] {worker_id}: Processing data batch {{i+1}}/{{duration}}")
    
    time.sleep(1)

print(f"[{{timestamp()}}] {worker_id}: COMPLETED {{task_type}}")
'''
    
    script_path.write_text(script_content)
    script_path.chmod(0o755)
    return script_path

def run_parallel_proof():
    """Run the definitive parallel execution proof"""
    print("="*80)
    print("PARALLEL EXECUTION PROOF")
    print("="*80)
    print("If execution is TRULY parallel, you will see:")
    print("1. All workers starting within milliseconds of each other")
    print("2. Interleaved output from different workers")
    print("3. Main thread continuing to work while sub-processes run")
    print("4. All workers finishing at different times based on their duration")
    print("="*80)
    
    # Create workers with different tasks and durations
    workers = [
        ("Worker_A", "CALCULATION", 8),
        ("Worker_B", "FILE_ANALYSIS", 6),
        ("Worker_C", "API_CALLS", 7),
        ("Worker_D", "DATA_PROCESSING", 5),
    ]
    
    scripts = []
    for worker_id, task_type, duration in workers:
        script = create_worker_script(worker_id, task_type, duration)
        scripts.append((worker_id, script, duration))
    
    print(f"\n[{datetime.now().strftime('%H:%M:%S.%f')[:-3]}] MAIN: Launching all workers NOW...")
    print("-"*80)
    
    # Launch all workers SIMULTANEOUSLY
    processes = []
    start_time = time.time()
    
    for worker_id, script, duration in scripts:
        # Start without waiting - this is the key!
        proc = subprocess.Popen(
            ["python3", str(script)],
            stdout=None,  # Output goes directly to terminal
            stderr=None,  # So we see interleaved output
        )
        processes.append((worker_id, proc, duration))
        print(f"[{datetime.now().strftime('%H:%M:%S.%f')[:-3]}] MAIN: Launched {worker_id} (PID: {proc.pid})")
    
    print("-"*80)
    print("ALL WORKERS RUNNING IN PARALLEL - Watch the interleaved output below:")
    print("-"*80)
    
    # Main thread continues working
    for i in range(10):
        elapsed = time.time() - start_time
        
        # Check which processes are still running
        running = []
        finished = []
        for worker_id, proc, _ in processes:
            if proc.poll() is None:
                running.append(worker_id)
            else:
                finished.append(worker_id)
        
        print(f"[{datetime.now().strftime('%H:%M:%S.%f')[:-3]}] MAIN: Iteration {i+1} at {elapsed:.1f}s")
        print(f"[{datetime.now().strftime('%H:%M:%S.%f')[:-3]}] MAIN: Running: {running}")
        print(f"[{datetime.now().strftime('%H:%M:%S.%f')[:-3]}] MAIN: Finished: {finished}")
        
        # Main does some work
        time.sleep(1)
    
    # Wait for all to complete
    print("\n" + "-"*80)
    print("MAIN: Finished my work. Waiting for workers to complete...")
    print("-"*80)
    
    for worker_id, proc, _ in processes:
        proc.wait()
        print(f"[{datetime.now().strftime('%H:%M:%S.%f')[:-3]}] MAIN: {worker_id} has finished")
    
    total_time = time.time() - start_time
    
    print("\n" + "="*80)
    print("RESULTS:")
    print(f"Total execution time: {total_time:.2f} seconds")
    print(f"Expected if parallel: ~8 seconds (max duration)")
    print(f"Expected if sequential: 26 seconds (8+6+7+5)")
    print(f"Actual result: {'PARALLEL' if total_time < 12 else 'SEQUENTIAL'}")
    print("="*80)

def run_clear_demonstration():
    """Even clearer demonstration with live output"""
    print("\n" + "="*80)
    print("CRYSTAL CLEAR PARALLEL DEMONSTRATION")
    print("="*80)
    
    # Create a simple counter script
    counter_script = Path(".orchestrate/tests/parallel_proof/counter.py")
    counter_script.parent.mkdir(parents=True, exist_ok=True)
    
    counter_code = '''#!/usr/bin/env python3
import sys
import time
from datetime import datetime

worker_id = sys.argv[1]
count_to = int(sys.argv[2])

# Force immediate output
sys.stdout = sys.stderr

for i in range(1, count_to + 1):
    timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    print(f"[{timestamp}] {worker_id}: Count = {i}/{count_to}")
    time.sleep(0.5)

print(f"[{datetime.now().strftime('%H:%M:%S.%f')[:-3]}] {worker_id}: DONE!")
'''
    
    counter_script.write_text(counter_code)
    counter_script.chmod(0o755)
    
    print("Starting 3 counters that will count simultaneously...")
    print("If they run in PARALLEL, their counts will be INTERLEAVED")
    print("If they run SEQUENTIALLY, you'll see one finish before the next starts")
    print("-"*80)
    
    # Start 3 counters
    proc1 = subprocess.Popen(["python3", str(counter_script), "Counter_RED", "10"])
    proc2 = subprocess.Popen(["python3", str(counter_script), "Counter_BLUE", "8"])
    proc3 = subprocess.Popen(["python3", str(counter_script), "Counter_GREEN", "6"])
    
    print(f"Started Counter_RED (counting to 10)")
    print(f"Started Counter_BLUE (counting to 8)")
    print(f"Started Counter_GREEN (counting to 6)")
    print("-"*80)
    print("WATCH THE OUTPUT - You should see all three counting at the same time:")
    print("-"*80)
    
    # Wait for all
    proc1.wait()
    proc2.wait()
    proc3.wait()
    
    print("-"*80)
    print("If you saw interleaved counting (RED, BLUE, GREEN mixed), that's PARALLEL!")
    print("If you saw one complete before the next started, that would be SEQUENTIAL")
    print("="*80)

if __name__ == "__main__":
    print("PARALLEL EXECUTION PROOF TEST")
    print("This will demonstrate unmistakable parallel execution\n")
    
    # Run the main proof
    run_parallel_proof()
    
    # Run the clear demonstration
    print("\n\nPress Enter for an even clearer demonstration...")
    try:
        input()
    except:
        pass
    
    run_clear_demonstration()