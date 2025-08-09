#!/usr/bin/env python3
"""
Rule Injection Hook - Periodically reminds about critical rules

This hook can be called to inject rule reminders into the conversation.
"""

import sys
from pathlib import Path

# Add brain directory to path
brain_path = Path(__file__).parent.parent.parent / "brain"
sys.path.insert(0, str(brain_path))

from rule_enforcer import RuleEnforcer

def inject_rules():
    """Inject critical rules reminder"""
    enforcer = RuleEnforcer()
    
    # Get core rules
    core_rules = enforcer.rules.get('core', {}).get('rules', [])
    
    if core_rules:
        print("\n" + "="*60)
        print("📋 CRITICAL RULES REMINDER")
        print("="*60)
        
        # Show top 5 core rules
        for i, rule in enumerate(core_rules[:5], 1):
            print(f"{i}. {rule}")
        
        # Check current session naming
        session_name = enforcer.enforce_session_naming()
        print(f"\n📅 Current session: agent-feedback/{session_name}/")
        
        # Reminder about documentation placement
        print("\n📚 Documentation Placement:")
        print("• Permanent knowledge → Docs/")
        print("• Transient reports → agent-feedback/")
        print("• Operational data → .orchestrator/")
        
        print("="*60 + "\n")
    
    return True

if __name__ == "__main__":
    inject_rules()
