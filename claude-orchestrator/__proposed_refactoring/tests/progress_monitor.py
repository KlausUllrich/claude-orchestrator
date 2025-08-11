#!/usr/bin/env python3
"""
Progress Monitor - Shows real-time progress bars for multiple agents
"""

import json
import time
from pathlib import Path
from datetime import datetime
import os
import sys

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def create_progress_bar(name, current, total, width=30):
    """Create a visual progress bar"""
    percent = current / total
    filled = int(width * percent)
    bar = '█' * filled + '░' * (width - filled)
    return f"{name:15} [{bar}] {current:3}/{total:3} ({percent*100:.0f}%)"

def monitor_progress():
    """Monitor agent progress files and display progress bars"""
    status_dir = Path(".orchestrate/tests/visible_parallel/status")
    
    agents = {
        "agent_red": {"total": 20, "current": 0, "status": "pending"},
        "agent_blue": {"total": 15, "current": 0, "status": "pending"},
        "agent_green": {"total": 10, "current": 0, "status": "pending"},
        "agent_yellow": {"total": 12, "current": 0, "status": "pending"}
    }
    
    print("="*60)
    print("PARALLEL AGENT PROGRESS MONITOR")
    print("="*60)
    print("Waiting for agents to start...")
    print()
    
    all_complete = False
    iteration = 0
    
    while not all_complete:
        iteration += 1
        clear_screen()
        
        print("="*60)
        print(f"PARALLEL AGENT PROGRESS MONITOR - Update #{iteration}")
        print(f"Time: {datetime.now().strftime('%H:%M:%S.%f')[:-3]}")
        print("="*60)
        print()
        
        # Check each agent's status
        for agent_name in agents:
            status_file = status_dir / f"{agent_name}.json"
            
            if status_file.exists():
                try:
                    with open(status_file, 'r') as f:
                        status_data = json.load(f)
                    
                    agents[agent_name]["current"] = status_data.get("progress", 0)
                    agents[agent_name]["status"] = status_data.get("status", "running")
                    
                except:
                    pass
        
        # Display progress bars
        print("AGENT PROGRESS:")
        print("-"*60)
        for agent_name, agent_data in agents.items():
            bar = create_progress_bar(
                agent_name.upper(),
                agent_data["current"],
                agent_data["total"]
            )
            status_emoji = {
                "pending": "⏳",
                "running": "🔄",
                "completed": "✅"
            }.get(agent_data["status"], "❓")
            
            print(f"{status_emoji} {bar}")
        
        print("-"*60)
        
        # Check if all complete
        all_complete = all(
            agent["status"] == "completed" 
            for agent in agents.values()
        )
        
        # Show Claude's joke file if it exists
        joke_file = Path(".orchestrate/tests/visible_parallel/claude_jokes.txt")
        if joke_file.exists():
            print("\nCLAUDE'S LATEST JOKE:")
            print("-"*60)
            with open(joke_file, 'r') as f:
                lines = f.readlines()
                if lines:
                    # Show last 3 jokes
                    for line in lines[-3:]:
                        print(f"😄 {line.strip()}")
            print("-"*60)
        
        if not all_complete:
            time.sleep(1)
    
    print("\n" + "="*60)
    print("ALL AGENTS COMPLETED!")
    print("="*60)

if __name__ == "__main__":
    monitor_progress()