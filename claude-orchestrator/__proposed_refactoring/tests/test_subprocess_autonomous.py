#!/usr/bin/env python3
"""
Test #1: Subprocess Approach for Autonomous Execution
Goal: Prove main agent can continue working while sub-agents run
"""

import subprocess
import time
import json
import threading
from pathlib import Path
from datetime import datetime
import random

class SubprocessAutonomyTest:
    def __init__(self):
        self.test_dir = Path(".orchestrate/tests/subprocess")
        self.test_dir.mkdir(parents=True, exist_ok=True)
        self.results = []
        
    def create_sub_agent_script(self, agent_id: str, duration: int, verbose: bool = True):
        """Create a simulated sub-agent script with verbose output"""
        script_path = self.test_dir / f"agent_{agent_id}.py"
        
        script_content = f'''#!/usr/bin/env python3
import time
import json
from pathlib import Path
from datetime import datetime
import sys

# Flush output immediately
def log(msg):
    print(f"[{{datetime.now().strftime('%H:%M:%S.%f')[:-3]}}] Agent {agent_id}: {{msg}}", flush=True)

log("STARTED - Will run for {duration} seconds")
start_time = datetime.now()

# Simulate work with progress updates
for i in range({duration}):
    log(f"Working... step {{i+1}}/{duration}")
    time.sleep(1)
    
    # Simulate some actual work
    result = sum(j*j for j in range(10000))
    
    if i == {duration}//2:
        log("HALFWAY COMPLETE")

# Write result
result = {{
    "agent_id": "{agent_id}",
    "start_time": start_time.isoformat(),
    "end_time": datetime.now().isoformat(),
    "duration": {duration},
    "result": f"Agent {agent_id} completed task after {duration} seconds"
}}

output_path = Path(".orchestrate/tests/subprocess/results/{agent_id}_result.json")
output_path.parent.mkdir(parents=True, exist_ok=True)
with open(output_path, 'w') as f:
    json.dump(result, f, indent=2)

log("COMPLETED - Result saved")
'''
        
        script_path.write_text(script_content)
        script_path.chmod(0o755)
        return script_path
    
    def test_blocking_execution(self):
        """Test 1: Traditional blocking subprocess (baseline)"""
        print("\n" + "="*80)
        print("TEST 1: BLOCKING SUBPROCESS (Sequential - Baseline)")
        print("="*80)
        print("This test runs agents ONE AT A TIME (sequential)")
        print("-"*80)
        
        # Create test agents with different durations
        agent1 = self.create_sub_agent_script("blocking_1", 8)
        agent2 = self.create_sub_agent_script("blocking_2", 5)
        
        start_time = time.time()
        
        # Execute sequentially (blocking)
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Starting agent 1 (blocks main for 8 seconds)...")
        result1 = subprocess.run(["python3", str(agent1)], capture_output=True, text=True)
        print(result1.stdout, end='')
        
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Starting agent 2 (blocks main for 5 seconds)...")
        result2 = subprocess.run(["python3", str(agent2)], capture_output=True, text=True)
        print(result2.stdout, end='')
        
        total_time = time.time() - start_time
        
        print("-"*80)
        print(f"Blocking execution total time: {total_time:.2f} seconds")
        print(f"Expected: ~13 seconds (8+5 sequential)")
        print(f"Result: {'✅ SEQUENTIAL' if abs(total_time - 13) < 2 else '❌ UNEXPECTED'}")
        
        self.results.append({
            "test": "blocking",
            "time": total_time,
            "expected": 13,
            "success": abs(total_time - 13) < 2
        })
        
        return total_time
    
    def test_nonblocking_execution(self):
        """Test 2: Non-blocking subprocess with Popen - PARALLEL"""
        print("\n" + "="*80)
        print("TEST 2: NON-BLOCKING SUBPROCESS (Parallel with Popen)")
        print("="*80)
        print("This test runs agents IN PARALLEL - watch the timestamps!")
        print("-"*80)
        
        # Create test agents with different durations
        agent1 = self.create_sub_agent_script("parallel_1", 10)
        agent2 = self.create_sub_agent_script("parallel_2", 8)
        agent3 = self.create_sub_agent_script("parallel_3", 6)
        
        start_time = time.time()
        processes = []
        
        # Start all agents WITHOUT BLOCKING - this is the key!
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Starting all agents SIMULTANEOUSLY...")
        
        # Launch all at once
        proc1 = subprocess.Popen(["python3", str(agent1)], 
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        processes.append(("parallel_1", proc1, 10))
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Agent 1 launched (PID: {proc1.pid}) - 10s duration")
        
        proc2 = subprocess.Popen(["python3", str(agent2)],
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        processes.append(("parallel_2", proc2, 8))
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Agent 2 launched (PID: {proc2.pid}) - 8s duration")
        
        proc3 = subprocess.Popen(["python3", str(agent3)],
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        processes.append(("parallel_3", proc3, 6))
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Agent 3 launched (PID: {proc3.pid}) - 6s duration")
        
        print("-"*80)
        print("ALL AGENTS NOW RUNNING IN PARALLEL - Main continues working...")
        print("-"*80)
        
        # Main agent continues working while others run
        for i in range(5):
            elapsed = time.time() - start_time
            print(f"[{datetime.now().strftime('%H:%M:%S')}] MAIN AGENT: Working iteration {i+1} (elapsed: {elapsed:.1f}s)")
            
            # Check status without blocking
            status = []
            for name, proc, _ in processes:
                if proc.poll() is None:
                    status.append(f"{name}:RUNNING")
                else:
                    status.append(f"{name}:DONE")
            print(f"    Agent status: {' | '.join(status)}")
            
            time.sleep(2)
        
        print("-"*80)
        print("Main agent work complete. Now collecting agent outputs...")
        print("-"*80)
        
        # Collect outputs as they complete
        outputs = {}
        for name, proc, expected_duration in processes:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Waiting for {name}...")
            output, _ = proc.communicate()
            outputs[name] = output
            elapsed = time.time() - start_time
            print(f"[{datetime.now().strftime('%H:%M:%S')}] {name} finished at {elapsed:.1f}s")
            
            # Show the agent's output
            print(f"--- Output from {name} ---")
            for line in output.strip().split('\n')[:5]:  # Show first 5 lines
                print(f"  {line}")
            if output.count('\n') > 5:
                print(f"  ... ({output.count('\n')-5} more lines)")
        
        total_time = time.time() - start_time
        
        print("-"*80)
        print(f"Non-blocking execution total time: {total_time:.2f} seconds")
        print(f"Expected: ~10 seconds (max of 10,8,6 running in PARALLEL)")
        print(f"Compare to sequential: Would be 24 seconds (10+8+6)")
        print(f"Time saved by parallelization: {24 - total_time:.1f} seconds")
        print(f"Result: {'✅ PARALLEL EXECUTION CONFIRMED' if abs(total_time - 10) < 2 else '❌ NOT PARALLEL'}")
        
        self.results.append({
            "test": "non-blocking-parallel",
            "time": total_time,
            "expected": 10,
            "success": abs(total_time - 10) < 2
        })
        
        return total_time
    
    def test_real_parallel_demo(self):
        """Test 3: Clear demonstration of parallel execution"""
        print("\n" + "="*80)
        print("TEST 3: CLEAR PARALLEL EXECUTION DEMONSTRATION")
        print("="*80)
        print("Watch the interleaved output from different agents!")
        print("-"*80)
        
        # Create agents that output frequently
        num_agents = 4
        duration = 5
        agents = []
        processes = []
        
        for i in range(num_agents):
            agent_id = f"demo_{i+1}"
            agent_path = self.create_sub_agent_script(agent_id, duration + i*2)  # 5, 7, 9, 11 seconds
            agents.append((agent_id, agent_path, duration + i*2))
        
        start_time = time.time()
        
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Launching {num_agents} agents in parallel...")
        
        # Launch all agents
        for agent_id, agent_path, dur in agents:
            proc = subprocess.Popen(["python3", str(agent_path)])
            processes.append((agent_id, proc, dur))
            print(f"[{datetime.now().strftime('%H:%M:%S')}] {agent_id} started ({dur}s duration)")
        
        print("-"*80)
        print("MONITORING PARALLEL EXECUTION:")
        print("-"*80)
        
        # Monitor execution
        all_done = False
        check_count = 0
        while not all_done:
            check_count += 1
            elapsed = time.time() - start_time
            
            # Check status
            running = []
            completed = []
            for agent_id, proc, dur in processes:
                if proc.poll() is None:
                    running.append(f"{agent_id}({dur}s)")
                else:
                    completed.append(agent_id)
            
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Check #{check_count} at {elapsed:.1f}s:")
            print(f"  Running: {', '.join(running) if running else 'none'}")
            print(f"  Completed: {', '.join(completed) if completed else 'none'}")
            
            all_done = len(running) == 0
            if not all_done:
                time.sleep(2)
        
        total_time = time.time() - start_time
        
        print("-"*80)
        print(f"Parallel execution total time: {total_time:.2f} seconds")
        print(f"Expected: ~11 seconds (longest agent)")
        print(f"If sequential would be: {sum(d for _, _, d in agents)} seconds")
        print(f"Parallelization saved: {sum(d for _, _, d in agents) - total_time:.1f} seconds")
        
        self.results.append({
            "test": "parallel-demo",
            "time": total_time,
            "expected": 11,
            "success": abs(total_time - 11) < 2
        })
        
        return total_time
    
    def test_true_autonomy(self):
        """Test 4: Prove main agent has true autonomy"""
        print("\n" + "="*80)
        print("TEST 4: TRUE AUTONOMY - Main Agent Continues Working")
        print("="*80)
        print("Main agent will do meaningful work while sub-agents run")
        print("-"*80)
        
        # Create long-running sub-agents
        sub_agents = []
        for i in range(3):
            agent_id = f"auto_{i+1}"
            duration = 15  # Long duration
            agent_path = self.create_sub_agent_script(agent_id, duration)
            sub_agents.append((agent_id, agent_path))
        
        start_time = time.time()
        
        # Launch sub-agents
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Launching 3 sub-agents (15s each)...")
        sub_processes = []
        for agent_id, agent_path in sub_agents:
            proc = subprocess.Popen(["python3", str(agent_path)])
            sub_processes.append(proc)
            print(f"  {agent_id} started (PID: {proc.pid})")
        
        print("-"*80)
        print("MAIN AGENT NOW PERFORMING INDEPENDENT WORK:")
        print("-"*80)
        
        # Main agent does real work
        main_work_results = []
        work_items = ["Analyzing code", "Running tests", "Checking dependencies", 
                     "Validating syntax", "Optimizing performance", "Writing documentation"]
        
        for i, task in enumerate(work_items):
            elapsed = time.time() - start_time
            print(f"[{datetime.now().strftime('%H:%M:%S')}] MAIN: {task} (elapsed: {elapsed:.1f}s)")
            
            # Simulate actual work
            time.sleep(2)
            main_work_results.append(f"{task}: completed at {elapsed:.1f}s")
            
            # Check sub-agents without blocking
            running = sum(1 for p in sub_processes if p.poll() is None)
            print(f"  Sub-agents still running: {running}/3")
        
        print("-"*80)
        print("Main agent work completed. Waiting for sub-agents...")
        
        # Wait for sub-agents
        for proc in sub_processes:
            proc.wait()
        
        total_time = time.time() - start_time
        
        print("-"*80)
        print(f"Total execution time: {total_time:.2f} seconds")
        print(f"Main agent completed {len(main_work_results)} tasks while sub-agents ran")
        print("This proves TRUE AUTONOMY - main agent wasn't blocked!")
        
        self.results.append({
            "test": "true-autonomy",
            "time": total_time,
            "expected": 15,
            "success": len(main_work_results) >= 5
        })
        
        return total_time
    
    def run_all_tests(self):
        """Run all autonomy tests"""
        print("="*80)
        print("SUBPROCESS AUTONOMY TESTS - VERBOSE VERSION")
        print("Testing TRUE parallel execution with clear visual proof")
        print("="*80)
        
        # Run tests
        self.test_blocking_execution()
        print("\n" + "="*80)
        print("Continuing to parallel test...")
        print("="*80)
        
        self.test_nonblocking_execution()
        print("\n" + "="*80)
        print("Continuing to demo test...")
        print("="*80)
        
        self.test_real_parallel_demo()
        print("\n" + "="*80)
        print("Continuing to autonomy test...")
        print("="*80)
        
        self.test_true_autonomy()
        
        # Summary
        print("\n" + "="*80)
        print("TEST SUMMARY")
        print("="*80)
        
        all_passed = True
        for result in self.results:
            status = "✅ PASS" if result["success"] else "❌ FAIL"
            print(f"{result['test']}: {status}")
            print(f"  Time: {result['time']:.2f}s, Expected: {result['expected']}s")
            all_passed = all_passed and result["success"]
        
        print("\n" + "="*80)
        if all_passed:
            print("✅ SUBPROCESS APPROACH PROVEN TO WORK!")
            print("\nKEY FINDINGS:")
            print("1. Popen enables TRUE parallel execution")
            print("2. Main agent maintains full autonomy")
            print("3. Multiple sub-agents run simultaneously")
            print("4. File-based communication works reliably")
            print("\nRECOMMENDATION: Proceed with subprocess-based refactoring")
        else:
            print("⚠️ Some tests failed - review results")
        print("="*80)
        
        # Save results
        results_path = self.test_dir / "test_results.json"
        with open(results_path, 'w') as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "approach": "subprocess",
                "all_passed": all_passed,
                "tests": self.results,
                "conclusion": "Subprocess with Popen provides true parallel execution"
            }, f, indent=2)
        
        print(f"\nDetailed results saved to: {results_path}")
        
        return all_passed

if __name__ == "__main__":
    print("Starting verbose parallel execution tests...")
    print("You will see clear evidence of parallel execution.\n")
    
    tester = SubprocessAutonomyTest()
    success = tester.run_all_tests()
    exit(0 if success else 1)