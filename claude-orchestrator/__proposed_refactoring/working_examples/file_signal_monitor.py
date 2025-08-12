#!/usr/bin/env python3
"""
Monitor for File-Based Signaling Test

Displays real-time status of agents coordinating via file signals
"""

import json
import time
from pathlib import Path
from datetime import datetime

class SignalMonitor:
    def __init__(self):
        self.base_dir = Path('.orchestrate/tests/file_signaling')
        self.signal_dir = self.base_dir / 'signals'
        self.status_dir = self.base_dir / 'status'
        
    def get_agent_status(self, agent_name):
        """Read agent's current status"""
        status_file = self.status_dir / f"{agent_name}.json"
        if status_file.exists():
            try:
                return json.loads(status_file.read_text())
            except:
                return {"state": "unknown", "message": "Cannot read status"}
        return {"state": "not_started", "message": "Not yet started"}
        
    def get_signals(self):
        """Get all active signals"""
        if not self.signal_dir.exists():
            return []
            
        signals = []
        for signal_file in self.signal_dir.glob("*.signal"):
            try:
                signal_data = json.loads(signal_file.read_text())
                signals.append(f"{signal_data['from']} → {signal_data['to']}")
            except:
                signals.append(signal_file.stem)
        return signals
        
    def display_status(self):
        """Display current status of all agents"""
        # Clear screen (Unix/Linux)
        print("\033[2J\033[H", end="")
        
        print("=" * 70)
        print(f"📡 FILE-BASED SIGNALING MONITOR - {datetime.now().strftime('%H:%M:%S')}")
        print("=" * 70)
        
        # Expected agents
        agents = ["agent_alpha", "agent_beta", "agent_gamma", "agent_delta"]
        
        print("\n📊 AGENT STATUS:")
        print("-" * 50)
        
        for agent in agents:
            status = self.get_agent_status(agent)
            state = status.get("state", "unknown")
            message = status.get("message", "")
            progress = status.get("progress", 0)
            
            # Status emoji
            emoji = {
                "not_started": "⏳",
                "waiting": "🔄",
                "signals_received": "✔️",
                "running": "🏃",
                "signaling": "📤",
                "completed": "✅",
                "unknown": "❓"
            }.get(state, "❓")
            
            # Progress bar
            bar_length = 20
            filled = int(bar_length * progress / 100)
            bar = "█" * filled + "░" * (bar_length - filled)
            
            print(f"{emoji} {agent:15} [{bar}] {progress:3}% - {message[:30]}")
            
        # Display active signals
        print("\n🚦 ACTIVE SIGNALS:")
        print("-" * 50)
        
        signals = self.get_signals()
        if signals:
            for signal in signals:
                print(f"  📨 {signal}")
        else:
            print("  No active signals")
            
        print("\n" + "=" * 70)
        
    def run(self):
        """Main monitoring loop"""
        print("Starting File Signal Monitor...")
        print("Waiting for agents to start...")
        
        try:
            while True:
                self.display_status()
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n\nMonitor stopped.")
            return 0

def main():
    monitor = SignalMonitor()
    return monitor.run()

if __name__ == "__main__":
    main()