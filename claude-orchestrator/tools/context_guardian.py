#!/usr/bin/env python3
"""
Context Guardian - Monitor and prevent context overflow in Claude sessions

This module tracks token usage and provides warnings before context limits are hit.
"""

import os
import sys
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Configuration
DEFAULT_MAX_TOKENS = 200000  # Claude's approximate context limit
WARNING_LEVELS = [70, 80, 90]  # Percentage thresholds
CHECKPOINT_LEVEL = 80  # Auto-checkpoint at this level

class ContextMonitor:
    """Monitors context usage and provides warnings"""
    
    def __init__(self, max_tokens: int = DEFAULT_MAX_TOKENS):
        self.max_tokens = max_tokens
        self.current_tokens = 0
        self.session_start = datetime.now()
        self.checkpoints = []
        self.warnings_issued = set()
        
        # Create state directory
        self.state_dir = Path.home() / '.claude-orchestrate'
        self.state_dir.mkdir(exist_ok=True)
        
        # State file for persistence
        self.state_file = self.state_dir / 'context_state.json'
        self.load_state()
    
    def estimate_tokens(self, text: str) -> int:
        """
        Estimate token count for text.
        Rough approximation: 1 token ≈ 4 characters for English text
        """
        # More accurate estimation based on common patterns
        # Average English word is ~4.7 characters, ~1.3 tokens per word
        words = len(text.split())
        chars = len(text)
        
        # Use combination of methods for better accuracy
        token_estimate = max(
            chars / 4,  # Character-based estimate
            words * 1.3  # Word-based estimate
        )
        
        return int(token_estimate)
    
    def add_content(self, content: str, content_type: str = "message") -> Dict:
        """Add content and check context usage"""
        tokens = self.estimate_tokens(content)
        self.current_tokens += tokens
        
        percentage = (self.current_tokens / self.max_tokens) * 100
        
        result = {
            "tokens_added": tokens,
            "total_tokens": self.current_tokens,
            "percentage": percentage,
            "warnings": [],
            "action_required": None
        }
        
        # Check warning levels
        for level in WARNING_LEVELS:
            if percentage >= level and level not in self.warnings_issued:
                self.warnings_issued.add(level)
                result["warnings"].append(f"Context at {level}% capacity!")
                
                if level == 70:
                    result["action_required"] = "Consider wrapping up current work"
                elif level == 80:
                    result["action_required"] = "Creating checkpoint - prepare for handover"
                    self.create_checkpoint()
                elif level == 90:
                    result["action_required"] = "CRITICAL - Initiate emergency handover!"
        
        self.save_state()
        return result
    
    def create_checkpoint(self) -> str:
        """Create a checkpoint of current session state"""
        checkpoint = {
            "timestamp": datetime.now().isoformat(),
            "tokens": self.current_tokens,
            "percentage": (self.current_tokens / self.max_tokens) * 100,
            "session_duration": str(datetime.now() - self.session_start)
        }
        
        self.checkpoints.append(checkpoint)
        
        # Save checkpoint to file
        checkpoint_file = self.state_dir / f"checkpoint_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(checkpoint_file, 'w') as f:
            json.dump(checkpoint, f, indent=2)
        
        print(f"✅ Checkpoint created: {checkpoint_file}")
        return str(checkpoint_file)
    
    def get_status(self) -> Dict:
        """Get current context status"""
        percentage = (self.current_tokens / self.max_tokens) * 100
        
        return {
            "current_tokens": self.current_tokens,
            "max_tokens": self.max_tokens,
            "percentage": round(percentage, 2),
            "remaining_tokens": self.max_tokens - self.current_tokens,
            "session_duration": str(datetime.now() - self.session_start),
            "checkpoints": len(self.checkpoints),
            "status": self._get_status_level(percentage)
        }
    
    def _get_status_level(self, percentage: float) -> str:
        """Determine status level based on percentage"""
        if percentage < 50:
            return "🟢 Healthy"
        elif percentage < 70:
            return "🟡 Moderate"
        elif percentage < 80:
            return "🟠 Warning"
        elif percentage < 90:
            return "🔴 Critical"
        else:
            return "💀 Overflow Imminent"
    
    def save_state(self):
        """Save current state to file"""
        state = {
            "current_tokens": self.current_tokens,
            "session_start": self.session_start.isoformat(),
            "checkpoints": self.checkpoints,
            "warnings_issued": list(self.warnings_issued)
        }
        
        with open(self.state_file, 'w') as f:
            json.dump(state, f, indent=2)
    
    def load_state(self):
        """Load state from file if exists"""
        if self.state_file.exists():
            try:
                with open(self.state_file, 'r') as f:
                    state = json.load(f)
                    self.current_tokens = state.get("current_tokens", 0)
                    self.session_start = datetime.fromisoformat(state.get("session_start", datetime.now().isoformat()))
                    self.checkpoints = state.get("checkpoints", [])
                    self.warnings_issued = set(state.get("warnings_issued", []))
                    print(f"📂 Loaded existing session state: {self.current_tokens} tokens")
            except Exception as e:
                print(f"⚠️ Could not load state: {e}")
    
    def reset(self):
        """Reset the monitor for a new session"""
        self.current_tokens = 0
        self.session_start = datetime.now()
        self.checkpoints = []
        self.warnings_issued = set()
        self.save_state()
        print("🔄 Context monitor reset for new session")


def interactive_mode():
    """Run in interactive monitoring mode"""
    monitor = ContextMonitor()
    
    print("🛡️ Context Guardian - Interactive Mode")
    print("=" * 50)
    print(f"Max tokens: {monitor.max_tokens:,}")
    print(f"Current tokens: {monitor.current_tokens:,}")
    print("=" * 50)
    print("\nCommands:")
    print("  status - Show current status")
    print("  add <text> - Add text and check context")
    print("  checkpoint - Create checkpoint")
    print("  reset - Reset for new session")
    print("  quit - Exit monitor")
    print()
    
    while True:
        try:
            command = input("guardian> ").strip()
            
            if command == "quit":
                break
            elif command == "status":
                status = monitor.get_status()
                print(f"\n{status['status']}")
                print(f"Tokens: {status['current_tokens']:,} / {status['max_tokens']:,} ({status['percentage']}%)")
                print(f"Remaining: {status['remaining_tokens']:,}")
                print(f"Session duration: {status['session_duration']}")
                print(f"Checkpoints: {status['checkpoints']}")
            elif command == "checkpoint":
                monitor.create_checkpoint()
            elif command == "reset":
                monitor.reset()
            elif command.startswith("add "):
                text = command[4:]
                result = monitor.add_content(text)
                print(f"Added {result['tokens_added']} tokens (Total: {result['total_tokens']:,} - {result['percentage']:.1f}%)")
                if result['warnings']:
                    for warning in result['warnings']:
                        print(f"⚠️ {warning}")
                if result['action_required']:
                    print(f"🔔 ACTION: {result['action_required']}")
            else:
                print("Unknown command. Try 'status', 'add <text>', 'checkpoint', 'reset', or 'quit'")
        except KeyboardInterrupt:
            print("\n👋 Exiting...")
            break
        except Exception as e:
            print(f"Error: {e}")


def test_mode():
    """Test the context monitoring with sample data"""
    monitor = ContextMonitor(max_tokens=10000)  # Small limit for testing
    
    print("🧪 Context Guardian - Test Mode")
    print("=" * 50)
    
    # Simulate a session with increasing content
    test_texts = [
        "Starting a new game development session. Working on player controller.",
        "Adding movement mechanics with WASD input and jumping with spacebar. " * 50,
        "Implementing enemy AI with pathfinding and state machines. " * 100,
        "Creating particle effects for explosions and magic spells. " * 150,
        "Debugging collision detection issues with the physics engine. " * 200,
    ]
    
    for i, text in enumerate(test_texts, 1):
        print(f"\n📝 Adding content block {i}...")
        result = monitor.add_content(text)
        
        print(f"   Tokens: {result['tokens_added']:,} added")
        print(f"   Total: {result['total_tokens']:,} ({result['percentage']:.1f}%)")
        
        if result['warnings']:
            for warning in result['warnings']:
                print(f"   ⚠️ {warning}")
        
        if result['action_required']:
            print(f"   🔔 {result['action_required']}")
        
        time.sleep(0.5)  # Brief pause for readability
    
    print("\n" + "=" * 50)
    print("📊 Final Status:")
    status = monitor.get_status()
    print(f"   {status['status']}")
    print(f"   Total tokens: {status['current_tokens']:,} / {status['max_tokens']:,}")
    print(f"   Checkpoints created: {status['checkpoints']}")
    print("=" * 50)


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Context Guardian - Monitor LLM context usage")
    parser.add_argument("--test", action="store_true", help="Run in test mode")
    parser.add_argument("--watch", action="store_true", help="Run in watch mode (interactive)")
    parser.add_argument("--status", action="store_true", help="Show current status and exit")
    parser.add_argument("--reset", action="store_true", help="Reset monitor for new session")
    parser.add_argument("--max-tokens", type=int, default=DEFAULT_MAX_TOKENS, 
                       help=f"Maximum token limit (default: {DEFAULT_MAX_TOKENS:,})")
    
    args = parser.parse_args()
    
    if args.test:
        test_mode()
    elif args.watch:
        interactive_mode()
    elif args.status:
        monitor = ContextMonitor(max_tokens=args.max_tokens)
        status = monitor.get_status()
        print(f"\n{status['status']}")
        print(f"Tokens: {status['current_tokens']:,} / {status['max_tokens']:,} ({status['percentage']}%)")
        print(f"Remaining: {status['remaining_tokens']:,}")
        print(f"Session duration: {status['session_duration']}")
        print(f"Checkpoints: {status['checkpoints']}")
    elif args.reset:
        monitor = ContextMonitor(max_tokens=args.max_tokens)
        monitor.reset()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
