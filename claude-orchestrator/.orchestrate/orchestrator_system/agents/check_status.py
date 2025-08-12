#!/usr/bin/env python3
import json
from pathlib import Path
from datetime import datetime

def check_status():
    workspace = Path(".orchestrate/orchestrator_system")
    status_dir = workspace / "status"
    
    print("=" * 60)
    print("📊 AGENT STATUS REPORT")
    print("=" * 60)
    
    for agent_id in ["agent1", "agent2", "agent3"]:
        status_file = status_dir / f"{agent_id}.json"
        
        if status_file.exists():
            try:
                status = json.loads(status_file.read_text())
                
                print(f"\n🤖 {agent_id.upper()}")
                print(f"   Status: {status.get('status', 'unknown')}")
                print(f"   Task: {status.get('task', 'none')[:60]}...")
                
                if status.get('started'):
                    print(f"   Started: {status['started']}")
                if status.get('completed'):
                    print(f"   Completed: {status['completed']}")
                if status.get('output_file'):
                    print(f"   Output: {status['output_file']}")
            except:
                print(f"\n🤖 {agent_id.upper()}: No status available")
        else:
            print(f"\n🤖 {agent_id.upper()}: Ready (no tasks yet)")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    check_status()
