#!/usr/bin/env python3
import sys
import subprocess
import json
from pathlib import Path

def resume_agent(agent_id, task):
    workspace = Path(".orchestrate/orchestrator_system")
    session_file = workspace / "sessions" / f"{agent_id}_session.txt"
    output_file = workspace / "outputs" / f"{agent_id}_latest.txt"
    
    if session_file.exists():
        session_id = session_file.read_text().strip()
        if session_id:
            print(f"📂 Resuming session {session_id[:8]}... for {agent_id}")
            cmd = f'claude -r {session_id} -p "{task}" --output-format json > {output_file} 2>&1'
        else:
            print(f"⚠️ No session to resume for {agent_id}, starting fresh")
            cmd = f'claude -p "{task}" --output-format json > {output_file} 2>&1'
    else:
        print(f"🆕 Starting new session for {agent_id}")
        cmd = f'claude -p "{task}" --output-format json > {output_file} 2>&1'
    
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    # Parse output
    try:
        output_data = json.loads(output_file.read_text())
        print(f"✅ {agent_id} completed with context!")
        print(f"📝 Result: {output_data.get('result', 'No result')[:200]}...")
        
        # Update session
        new_session = output_data.get("session_id", "")
        if new_session:
            session_file.parent.mkdir(exist_ok=True)
            session_file.write_text(new_session)
    except:
        print(f"✅ {agent_id} completed")
        print(f"📄 Output: {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: resume_agent.py <agent_id> <task>")
        sys.exit(1)
    
    resume_agent(sys.argv[1], sys.argv[2])
