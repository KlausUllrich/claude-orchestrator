#!/usr/bin/env python3
"""
Create visible agent scripts that update progress files
"""

from pathlib import Path

def create_visible_agent(name: str, color: str, duration: int):
    """Create an agent that writes visible progress"""
    script_path = Path(f".orchestrate/tests/visible_parallel/{name}.py")
    script_path.parent.mkdir(parents=True, exist_ok=True)
    
    script_content = f'''#!/usr/bin/env python3
import json
import time
from pathlib import Path
from datetime import datetime

agent_name = "{name}"
color = "{color}"
duration = {duration}

status_file = Path(f".orchestrate/tests/visible_parallel/status/{{agent_name}}.json")
status_file.parent.mkdir(parents=True, exist_ok=True)

print(f"[{{datetime.now().strftime('%H:%M:%S')}}] {{agent_name.upper()}}: Starting {{duration}}s task")

for i in range(duration + 1):
    # Update status file
    status = {{
        "agent": agent_name,
        "color": color,
        "status": "running" if i < duration else "completed",
        "progress": i,
        "total": duration,
        "timestamp": datetime.now().isoformat(),
        "message": f"Processing step {{i}}/{{duration}}"
    }}
    
    with open(status_file, 'w') as f:
        json.dump(status, f, indent=2)
    
    if i % 3 == 0:
        print(f"[{{datetime.now().strftime('%H:%M:%S')}}] {{agent_name.upper()}}: Progress {{i}}/{{duration}}")
    
    if i < duration:
        time.sleep(1)

print(f"[{{datetime.now().strftime('%H:%M:%S')}}] {{agent_name.upper()}}: COMPLETED!")
'''
    
    script_path.write_text(script_content)
    script_path.chmod(0o755)
    return script_path

# Create the agents
agents = [
    ("agent_red", "red", 20),
    ("agent_blue", "blue", 15),
    ("agent_green", "green", 10),
    ("agent_yellow", "yellow", 12)
]

print("Creating visible agent scripts...")
for name, color, duration in agents:
    path = create_visible_agent(name, color, duration)
    print(f"Created {path} ({duration}s duration)")

print("\nAgents ready for parallel execution test!")
print("\nTo test:")
print("1. Run progress_monitor.py in one terminal")
print("2. Use Task tool to launch all agents in a single message")
print("3. Claude should tell jokes while agents run")