#!/usr/bin/env python3
"""
Claude Orchestrator System
One master orchestrator Claude with 3 sub-agent Claudes
"""

import subprocess
import json
import time
import os
from pathlib import Path
from datetime import datetime

class OrchestratorSystem:
    def __init__(self):
        self.workspace = Path(".orchestrate/orchestrator_system")
        self.agents_dir = self.workspace / "agents"
        self.outputs_dir = self.workspace / "outputs"
        self.status_dir = self.workspace / "status"
        
        # Create directories
        for dir in [self.agents_dir, self.outputs_dir, self.status_dir]:
            dir.mkdir(parents=True, exist_ok=True)
            
        # Agent configuration
        self.agents = {
            "agent1": {"status": "ready", "session": None, "current_task": None},
            "agent2": {"status": "ready", "session": None, "current_task": None},
            "agent3": {"status": "ready", "session": None, "current_task": None}
        }
        
        self.create_orchestrator_instructions()
        self.create_agent_launchers()
        
    def create_orchestrator_instructions(self):
        """Create instructions file for the orchestrator Claude"""
        instructions = '''# Orchestrator Instructions

You are the Master Orchestrator Claude. You have control over 3 sub-agent Claudes.

## Your Capabilities:

### 1. Launch Tasks on Sub-Agents
Use the Bash tool to execute these commands:

**Single Agent Task:**
```bash
python .orchestrate/orchestrator_system/agents/launch_agent.py agent1 "Your task here"
```

**Parallel Tasks (all agents):**
```bash
python .orchestrate/orchestrator_system/agents/launch_parallel.py "Task 1" "Task 2" "Task 3"
```

**Background Task:**
```bash
python .orchestrate/orchestrator_system/agents/launch_agent.py agent1 "Long running task" --background
```

### 2. Check Agent Status
```bash
python .orchestrate/orchestrator_system/agents/check_status.py
```

### 3. Read Agent Output
```bash
cat .orchestrate/orchestrator_system/outputs/agent1_latest.txt
```

### 4. Resume Agent Session (for context sharing)
```bash
python .orchestrate/orchestrator_system/agents/resume_agent.py agent1 "Continue previous task"
```

### 5. Clear Agent Output
```bash
python .orchestrate/orchestrator_system/agents/clear_outputs.py
```

## Agent Management Commands:

- **LAUNCH**: Start a task on specific agent
- **STATUS**: Check what each agent is doing
- **READ**: Get results from completed tasks
- **PARALLEL**: Launch all 3 agents simultaneously
- **STOP**: Kill a running agent task

## Example Workflows:

### Parallel Code Review:
```bash
python .orchestrate/orchestrator_system/agents/launch_parallel.py \
  "Review code for bugs" \
  "Check code style and formatting" \
  "Suggest performance improvements"
```

### Sequential Processing:
```bash
# Agent 1 analyzes
python .orchestrate/orchestrator_system/agents/launch_agent.py agent1 "Analyze the requirements"
# Wait and read output
cat .orchestrate/orchestrator_system/outputs/agent1_latest.txt
# Agent 2 continues with context
python .orchestrate/orchestrator_system/agents/resume_agent.py agent2 "Based on analysis, create implementation plan"
```

### Background Processing:
```bash
# Launch long task in background
python .orchestrate/orchestrator_system/agents/launch_agent.py agent3 "Process large dataset" --background
# Continue with other work while agent3 processes
```

## Important Notes:
- Agents run as separate Claude instances
- Each agent maintains its own context/session
- Use JSON format for structured communication
- Monitor status regularly for long-running tasks
- Background tasks continue even if you move to other work

You are now ready to orchestrate! The user will give you tasks to distribute among your sub-agents.
'''
        
        instructions_file = self.workspace / "ORCHESTRATOR_README.md"
        instructions_file.write_text(instructions)
        print(f"Created orchestrator instructions: {instructions_file}")
        
    def create_agent_launchers(self):
        """Create Python scripts for agent control"""
        
        # launch_agent.py
        launch_agent_script = '''#!/usr/bin/env python3
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
'''
        
        # launch_parallel.py
        launch_parallel_script = '''#!/usr/bin/env python3
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
    
    print("\\n⏳ Waiting for agents to complete...")
    
    # Wait for all to complete
    for agent_id, proc, output_file in procs:
        proc.wait()
        print(f"✅ {agent_id} completed - Output: {output_file}")
    
    print("\\n🎉 All agents completed!")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: launch_parallel.py <task1> <task2> <task3>")
        sys.exit(1)
    
    launch_parallel(sys.argv[1], sys.argv[2], sys.argv[3])
'''

        # check_status.py
        check_status_script = '''#!/usr/bin/env python3
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
                
                print(f"\\n🤖 {agent_id.upper()}")
                print(f"   Status: {status.get('status', 'unknown')}")
                print(f"   Task: {status.get('task', 'none')[:60]}...")
                
                if status.get('started'):
                    print(f"   Started: {status['started']}")
                if status.get('completed'):
                    print(f"   Completed: {status['completed']}")
                if status.get('output_file'):
                    print(f"   Output: {status['output_file']}")
            except:
                print(f"\\n🤖 {agent_id.upper()}: No status available")
        else:
            print(f"\\n🤖 {agent_id.upper()}: Ready (no tasks yet)")
    
    print("\\n" + "=" * 60)

if __name__ == "__main__":
    check_status()
'''

        # resume_agent.py
        resume_agent_script = '''#!/usr/bin/env python3
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
'''

        # clear_outputs.py
        clear_outputs_script = '''#!/usr/bin/env python3
from pathlib import Path

workspace = Path(".orchestrate/orchestrator_system")
outputs_dir = workspace / "outputs"

for file in outputs_dir.glob("*.txt"):
    file.unlink()
    print(f"🗑️ Cleared: {file.name}")

print("✨ All outputs cleared!")
'''
        
        # Save all scripts
        scripts = {
            "launch_agent.py": launch_agent_script,
            "launch_parallel.py": launch_parallel_script,
            "check_status.py": check_status_script,
            "resume_agent.py": resume_agent_script,
            "clear_outputs.py": clear_outputs_script
        }
        
        for name, content in scripts.items():
            script_path = self.agents_dir / name
            script_path.write_text(content)
            script_path.chmod(0o755)
            print(f"Created script: {script_path}")

def main():
    print("=" * 70)
    print("🚀 CLAUDE ORCHESTRATOR SYSTEM")
    print("=" * 70)
    
    system = OrchestratorSystem()
    
    print("\n✅ System initialized successfully!")
    print("\nTo start the orchestrator, run:")
    print("  claude --append-system-prompt 'You are an orchestrator managing 3 sub-agents. Read .orchestrate/orchestrator_system/ORCHESTRATOR_README.md for instructions.'")
    print("\nOr simply run:")
    print("  claude")
    print("\nThen tell Claude: 'You are my orchestrator. Read the orchestrator instructions and help me coordinate 3 sub-agents.'")
    
    print("\n" + "=" * 70)

if __name__ == "__main__":
    main()