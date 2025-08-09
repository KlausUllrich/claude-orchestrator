#!/usr/bin/env python3
"""
Context and Rule Check Hook - Lightweight hook for Claude sessions

This hook is a THIN WRAPPER that calls the actual rule enforcer.
The rules themselves are defined in claude-orchestrator/brain/rules/
This ensures a single source of truth for all rules.

How it works:
1. This hook is called periodically during Claude sessions
2. It imports the RuleEnforcer from the orchestrator tool
3. RuleEnforcer reads rules from YAML files
4. Rules are applied and reminders are shown
"""

import os
import sys
from pathlib import Path

# Find the orchestrator tool in our project
# This assumes .claude/hooks/ is in the project root
project_root = Path(__file__).parent.parent
orchestrator_path = project_root / "claude-orchestrator"

# Add orchestrator directories to Python path so we can import from them
brain_path = orchestrator_path / "brain"
tools_path = orchestrator_path / "tools"

sys.path.insert(0, str(brain_path))
sys.path.insert(0, str(tools_path))
sys.path.insert(0, str(orchestrator_path))  # Also add root for imports

def main():
    """
    Main function that performs two checks:
    1. Context usage (to prevent overflow)
    2. Rule enforcement (to maintain consistency)
    """
    
    print("\n🛡️ Claude Orchestrator - Session Check")
    print("-" * 60)
    
    # PART 1: Check context usage to prevent overflow
    try:
        # Add tools path and import
        sys.path.insert(0, str(tools_path))
        from context_guardian import ContextMonitor
        
        monitor = ContextMonitor()
        status = monitor.get_status()
        percentage = status['percentage']
        
        # Display context status with appropriate warning level
        if percentage < 50:
            print(f"📊 Context: {percentage:.1f}% - 🟢 Healthy")
        elif percentage < 70:
            print(f"📊 Context: {percentage:.1f}% - 🟡 Monitor usage")
        elif percentage < 80:
            print(f"⚠️ Context: {percentage:.1f}% - 🟠 WARNING: Approaching limit")
        elif percentage < 90:
            print(f"🔴 Context: {percentage:.1f}% - ❗ CRITICAL: Create checkpoint now!")
        else:
            print(f"💀 Context: {percentage:.1f}% - 🚨 EMERGENCY: Immediate handover needed!")
            print("\nSTOP adding content! Create handover document NOW!")
            return 1  # Exit with error
            
    except ImportError:
        print("⚠️ Context Guardian not found - skipping context check")
    except Exception as e:
        print(f"⚠️ Context check error: {e}")
    
    print("-" * 60)
    
    # PART 2: Enforce rules from the single source of truth
    try:
        # Add brain path and import the Rule Enforcer
        sys.path.insert(0, str(brain_path))
        from rule_enforcer import RuleEnforcer
        
        # Create enforcer instance - this loads all YAML rules
        enforcer = RuleEnforcer()
        
        print(f"📋 Rules loaded from: claude-orchestrator/brain/rules/")
        print(f"   Found {len(enforcer.rules)} rule sets")
        
        # Get the most important rules to remind about
        # The rules themselves are defined in the YAML files, not here!
        reminder = enforcer.inject_rules_reminder()
        if reminder:
            print(reminder)
        
        # Show current session folder (computed from rules)
        session_name = enforcer.enforce_session_naming()
        print(f"\n📁 Current session: agent-feedback/{session_name}/")
        
        # Quick validation examples
        print("\n🔍 Quick validation examples:")
        
        # Test some common naming patterns
        test_cases = [
            ("my-file.md", "✅"),        # Good: kebab-case
            ("my_file.md", "❌"),        # Bad: underscore
            ("MyFile.md", "❌"),         # Bad: uppercase
            ("README.md", "✅"),         # Good: allowed exception
        ]
        
        for filename, expected in test_cases:
            is_valid = enforcer.check_naming_convention(filename)
            symbol = "✅" if is_valid else "❌"
            print(f"   {symbol} {filename}")
        
    except ImportError:
        print("⚠️ Rule Enforcer not found - skipping rule check")
        print("   Make sure claude-orchestrator is properly installed")
    except Exception as e:
        print(f"⚠️ Rule enforcement error: {e}")
    
    print("-" * 60)
    print("💡 Tip: Rules are defined in claude-orchestrator/brain/rules/*.yaml")
    print("   Edit the YAML files to change rules (single source of truth)")
    print()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
