#!/usr/bin/env python3
"""
Test File-Based Signaling for Agent Coordination

This test demonstrates:
1. Agents communicating via signal files
2. Claude monitoring coordination without blocking
3. Agents waiting for signals before proceeding
"""

import json
import os
import sys
import time
from pathlib import Path
from datetime import datetime

class FileSignalingAgent:
    def __init__(self, name, color, duration, wait_for=None, signals_to=None):
        self.name = name
        self.color = color
        self.duration = duration
        self.wait_for = wait_for or []
        self.signals_to = signals_to or []
        
        # Setup paths
        self.base_dir = Path('.orchestrate/tests/file_signaling')
        self.signal_dir = self.base_dir / 'signals'
        self.status_dir = self.base_dir / 'status'
        
        # Create directories
        self.signal_dir.mkdir(parents=True, exist_ok=True)
        self.status_dir.mkdir(parents=True, exist_ok=True)
        
        # Define signal files
        self.my_signal = self.signal_dir / f"{self.name}_ready.signal"
        self.status_file = self.status_dir / f"{self.name}.json"
        
    def wait_for_signals(self):
        """Wait for required signals before starting work"""
        if not self.wait_for:
            return True
            
        self.update_status("waiting", f"Waiting for signals: {self.wait_for}")
        
        while True:
            all_ready = True
            for signal_name in self.wait_for:
                signal_file = self.signal_dir / f"{signal_name}_ready.signal"
                if not signal_file.exists():
                    all_ready = False
                    break
                    
            if all_ready:
                self.update_status("signals_received", f"All required signals received")
                return True
                
            time.sleep(0.5)
    
    def send_signals(self):
        """Send signals to dependent agents"""
        for signal_name in self.signals_to:
            self.my_signal.write_text(json.dumps({
                "from": self.name,
                "to": signal_name,
                "timestamp": datetime.now().isoformat(),
                "message": f"{self.name} is ready"
            }))
            
    def update_status(self, state, message="", progress=0):
        """Update status file for monitoring"""
        status = {
            "name": self.name,
            "state": state,
            "message": message,
            "progress": progress,
            "timestamp": datetime.now().isoformat()
        }
        self.status_file.write_text(json.dumps(status, indent=2))
        
    def run(self):
        """Main agent execution"""
        print(f"🎭 {self.name} starting...")
        
        # Phase 1: Wait for dependencies
        self.wait_for_signals()
        
        # Phase 2: Execute task
        self.update_status("running", f"Executing {self.duration}s task")
        
        for i in range(self.duration):
            progress = int((i / self.duration) * 100)
            self.update_status("running", f"Working... {i+1}/{self.duration}s", progress)
            time.sleep(1)
            
        # Phase 3: Signal completion
        self.update_status("signaling", "Sending completion signals")
        self.send_signals()
        
        # Phase 4: Complete
        self.update_status("completed", f"Task completed in {self.duration}s", 100)
        print(f"✅ {self.name} completed!")
        
        return 0

def main():
    """Parse arguments and run agent"""
    if len(sys.argv) < 4:
        print("Usage: python test_file_signaling.py <name> <color> <duration> [wait_for] [signals_to]")
        sys.exit(1)
        
    name = sys.argv[1]
    color = sys.argv[2]
    duration = int(sys.argv[3])
    
    # Parse dependencies
    wait_for = []
    signals_to = []
    
    if len(sys.argv) > 4:
        wait_for = sys.argv[4].split(',') if sys.argv[4] != 'none' else []
    if len(sys.argv) > 5:
        signals_to = sys.argv[5].split(',') if sys.argv[5] != 'none' else []
        
    # Create and run agent
    agent = FileSignalingAgent(name, color, duration, wait_for, signals_to)
    return agent.run()

if __name__ == "__main__":
    sys.exit(main())