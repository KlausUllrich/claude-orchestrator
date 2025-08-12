#!/usr/bin/env python3
import sys
import subprocess
import json
from pathlib import Path
from datetime import datetime

def launch_agent(agent_id, task, background=False):
    workspace = Path(".orchestrate/orchestrator_system")
    output_file = workspace / "outputs" / f"{agent_id}_latest.txt"
    status_file = workspace / "status" / f"{agent_id}.json"
    
    # Update status
    status = {
        "agent": agent_id,
        "task": task,
        "status": "running",
        "started": datetime.now().isoformat(),
        "output_file": str(output_file)
    }
    status_file.write_text(json.dumps(status, indent=2))
    
    # Launch Claude
    cmd = f'claude -p "{task}" --output-format json > {output_file} 2>&1'
    
    if background:
        subprocess.Popen(cmd, shell=True)
        print(f"✅ {agent_id} launched in background: {task[:50]}...")
    else:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        # Update status
        status["status"] = "completed"
        status["completed"] = datetime.now().isoformat()
        status_file.write_text(json.dumps(status, indent=2))
        
        # Parse and display result
        try:
            output_data = json.loads(output_file.read_text())
            print(f"✅ {agent_id} completed!")
            print(f"📝 Result: {output_data.get('result', 'No result')[:200]}...")
            print(f"📄 Full output: {output_file}")
            
            # Save session for potential resume
            session_file = workspace / "sessions" / f"{agent_id}_session.txt"
            session_file.parent.mkdir(exist_ok=True)
            session_file.write_text(output_data.get("session_id", ""))
        except:
            print(f"✅ {agent_id} completed (non-JSON output)")
            print(f"📄 Output saved to: {output_file}")
    
    return str(output_file)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: launch_agent.py <agent_id> <task> [--background]")
        sys.exit(1)
    
    agent_id = sys.argv[1]
    task = sys.argv[2]
    background = "--background" in sys.argv
    
    launch_agent(agent_id, task, background)
