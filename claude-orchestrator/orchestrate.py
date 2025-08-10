#!/usr/bin/env python3
"""
Claude Orchestrator - Main Entry Point

A portable orchestration system for managing LLM development.
"""

import os
import sys
import argparse
from pathlib import Path

# Add tools directory to path
sys.path.insert(0, str(Path(__file__).parent / "tools"))

def main():
    parser = argparse.ArgumentParser(
        description="Claude Orchestrator - Manage LLM development context and workflows"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Start command
    start_parser = subparsers.add_parser("start", help="Start orchestrator monitoring")
    
    # Status command
    status_parser = subparsers.add_parser("status", help="Show current status")
    
    # Enable command
    enable_parser = subparsers.add_parser("enable", help="Enable a component")
    enable_parser.add_argument("type", choices=["hook", "agent", "workflow"])
    enable_parser.add_argument("name", help="Name of component to enable")
    
    # Disable command
    disable_parser = subparsers.add_parser("disable", help="Disable a component")
    disable_parser.add_argument("type", choices=["hook", "agent", "workflow"])
    disable_parser.add_argument("name", help="Name of component to disable")
    
    # List command
    list_parser = subparsers.add_parser("list", help="List available components")
    list_parser.add_argument("type", choices=["hooks", "agents", "workflows", "all"])
    
    # Workflow command
    workflow_parser = subparsers.add_parser("workflow", help="Manage workflows")
    workflow_parser.add_argument("action", choices=["activate", "deactivate", "status"])
    workflow_parser.add_argument("name", nargs="?", help="Workflow name")
    
    # Handover command
    handover_parser = subparsers.add_parser("handover", help="Create session handover document")
    handover_parser.add_argument("--summary", help="Session summary", default="")
    
    # Session command
    session_parser = subparsers.add_parser("session", help="Manage session state")
    session_parser.add_argument("action", choices=["start", "status"], help="Session action")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Handle commands
    if args.command == "start":
        print("🚀 Starting Claude Orchestrator monitoring...")
        from context_guardian import interactive_mode
        interactive_mode()
    
    elif args.command == "status":
        print("📊 Claude Orchestrator Status")
        print("=" * 40)
        from context_guardian import ContextMonitor
        monitor = ContextMonitor()
        status = monitor.get_status()
        print(f"Context: {status['status']}")
        print(f"Tokens: {status['current_tokens']:,} / {status['max_tokens']:,} ({status['percentage']}%)")
        print(f"Session: {status['session_duration']}")
        
        # Check active workflow
        active_workflow = Path("workflows/active")
        if active_workflow.exists():
            workflow = active_workflow.resolve().name
            print(f"Workflow: {workflow}")
        else:
            print("Workflow: none")
    
    elif args.command == "enable":
        print(f"✅ Enabling {args.type}: {args.name}")
        # TODO: Implement component enabling
        print("   (Feature coming soon)")
    
    elif args.command == "disable":
        print(f"❌ Disabling {args.type}: {args.name}")
        # TODO: Implement component disabling
        print("   (Feature coming soon)")
    
    elif args.command == "list":
        if args.type in ["hooks", "all"]:
            print("\n📎 Available Hooks:")
            hooks_dir = Path("resource-library/hooks")
            if hooks_dir.exists():
                for category in hooks_dir.iterdir():
                    if category.is_dir():
                        print(f"  {category.name}/")
                        # TODO: List individual hooks
        
        if args.type in ["agents", "all"]:
            print("\n🤖 Available Agents:")
            agents_dir = Path("resource-library/agents")
            if agents_dir.exists():
                for agent in agents_dir.iterdir():
                    if agent.is_dir():
                        print(f"  - {agent.name}")
        
        if args.type in ["workflows", "all"]:
            print("\n🔄 Available Workflows:")
            workflows_dir = Path("workflows")
            if workflows_dir.exists():
                for workflow in workflows_dir.iterdir():
                    if workflow.is_dir() and workflow.name != "active":
                        print(f"  - {workflow.name}")
    
    elif args.command == "workflow":
        if args.action == "activate" and args.name:
            print(f"🔄 Activating workflow: {args.name}")
            workflow_path = Path(f"workflows/{args.name}")
            if workflow_path.exists():
                active_link = Path("workflows/active")
                if active_link.exists():
                    active_link.unlink()
                active_link.symlink_to(args.name)
                print(f"✅ Workflow '{args.name}' activated")
            else:
                print(f"❌ Workflow '{args.name}' not found")
        
        elif args.action == "status":
            active_workflow = Path("workflows/active")
            if active_workflow.exists():
                workflow = active_workflow.resolve().name
                print(f"Active workflow: {workflow}")
            else:
                print("No active workflow")
    
    elif args.command == "handover":
        # Simple command that just shows session info
        # The LLM will handle the actual handover creation
        import importlib.util
        spec = importlib.util.spec_from_file_location("handover_manager", 
                                                      Path(__file__).parent / "brain" / "handover-manager.py")
        handover_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(handover_module)
        manager = handover_module.HandoverManager()
        
        if args.summary == "info":
            # Just show session information
            print(manager.get_info_summary())
        elif args.summary == "gather":
            # Get raw data for LLM analysis
            import json
            info = manager.gather_session_info()
            print(json.dumps(info, indent=2, default=str))
        elif args.summary == "save":
            # Save handover content (reading from stdin)
            import sys
            content = sys.stdin.read()
            path = manager.archive_and_save_handover(content)
            print(f"✅ Handover saved to: {path}")
        else:
            # Default: show info and instructions
            print("📝 Handover Helper Tool")
            print("=" * 60)
            print("\nThis tool helps gather session information for handover creation.")
            print("\nUsage:")
            print("  python orchestrate.py handover info    - Show session summary")
            print("  python orchestrate.py handover gather  - Get JSON data for analysis")
            print("  python orchestrate.py handover save    - Save handover (from stdin)")
            print("\nThe LLM should use these commands to create comprehensive handovers.")
    
    elif args.command == "session":
        if args.action == "start":
            print("🚀 Starting new session...")
            import importlib.util
            spec = importlib.util.spec_from_file_location("handover_manager", 
                                                          Path(__file__).parent / "brain" / "handover-manager.py")
            handover_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(handover_module)
            manager = handover_module.HandoverManager()
            
            # Read the handover
            content = manager.read_handover()
            
            if content:
                print("\n" + "="*60)
                print("📋 Previous Session Handover:")
                print("="*60)
                # Show first part of handover (required reading and summary)
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    print(line)
                    if i > 50 and "## Next Session Goals" in line:
                        # Show goals section
                        for j in range(i, min(i+20, len(lines))):
                            if lines[j].startswith("##") and j > i:
                                break
                            print(lines[j])
                        break
                
                print("\n" + "="*60)
                print("✅ Session started. Review the full handover at: docs/status/handover-next.md")
                print("📚 Don't forget to read the required documents listed in the handover!")
            else:
                print("ℹ️ No previous handover found. Starting fresh session.")
                print("📚 Please read docs/read-first.md for required documentation.")
        
        elif args.action == "status":
            print("📊 Current session status")
            # Could add more session status info here
            print("   Use 'python orchestrate.py handover' to create a handover")
            print("   Use 'python orchestrate.py session start' to begin from handover")

if __name__ == "__main__":
    main()
