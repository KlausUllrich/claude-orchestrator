#!/usr/bin/env python3
import sys
import subprocess
import time
from pathlib import Path

def launch_parallel(task1, task2, task3):
    workspace = Path(".orchestrate/orchestrator_system")
    
    print("🚀 Launching 3 agents in parallel...")
    
    # Launch all three agents
    procs = []
    tasks = [task1, task2, task3]
    
    for i, task in enumerate(tasks, 1):
        agent_id = f"agent{i}"
        output_file = workspace / "outputs" / f"{agent_id}_latest.txt"
        
        cmd = f'claude -p "{task}" > {output_file} 2>&1'
        proc = subprocess.Popen(cmd, shell=True)
        procs.append((agent_id, proc, output_file))
        
        print(f"  ➤ {agent_id}: {task[:50]}...")
    
    print("\n⏳ Waiting for agents to complete...")
    
    # Wait for all to complete
    for agent_id, proc, output_file in procs:
        proc.wait()
        print(f"✅ {agent_id} completed - Output: {output_file}")
    
    print("\n🎉 All agents completed!")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: launch_parallel.py <task1> <task2> <task3>")
        sys.exit(1)
    
    launch_parallel(sys.argv[1], sys.argv[2], sys.argv[3])
