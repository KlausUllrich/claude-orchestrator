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
    session_parser.add_argument("action", choices=["start", "status", "end"], help="Session action")
    session_parser.add_argument("--no-cleanup", action="store_true", help="Skip maintenance analysis")
    session_parser.add_argument("--no-git", action="store_true", help="Skip git operations")
    session_parser.add_argument("--emergency", action="store_true", help="Emergency mode - handover only")
    
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
        
        elif args.action == "end":
            import json
            import importlib.util
            from datetime import datetime
            
            print("🏁 Session End Process")
            print("=" * 60)
            
            if args.emergency:
                print("⚠️ EMERGENCY MODE - Creating handover only")
                print("\nPlease use the /handover command to create and save a handover.")
                print("This will preserve critical session information.")
                return
            
            # Load session end manager
            spec = importlib.util.spec_from_file_location("session_end_manager", 
                                                          Path(__file__).parent / "brain" / "session-end-manager.py")
            session_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(session_module)
            manager = session_module.SessionEndManager()
            
            # Get available maintenance tasks
            tasks_path = Path(manager.get_task_documents_path())
            # For testing: Start with just unreferenced_documents_check
            # TODO: Re-enable all tasks after debugging
            task_files = ["unreferenced_documents_check"]  # Simplified for testing
            # Full list for later:
            # task_files = [f.stem for f in tasks_path.glob("*.md") 
            #              if not f.stem.startswith("DOCUMENT_TYPE") and f.stem != "handover_validation_check"]
            
            # Use session-reports directory for decisions (same place as findings)
            reports_dir = Path(manager.get_reports_directory())
            reports_dir.mkdir(parents=True, exist_ok=True)
            decisions_dir = reports_dir  # Keep decisions with findings
            session_id = datetime.now().strftime("session-%Y%m%d-%H%M%S")
            
            # Provide orchestration instructions
            print("\n" + "="*60)
            print("🎯 ORCHESTRATION INSTRUCTIONS FOR CLAUDE")
            print("="*60)
            
            orchestration_data = {
                "workflow": "session-end",
                "session_id": session_id,
                "decisions_dir": str(decisions_dir),
                "phases": [],
                "maintenance_tasks": task_files if not args.no_cleanup else [],
                "git_enabled": not args.no_git
            }
            
            print("\n📋 PHASE 1: HANDOVER CREATION (SEQUENTIAL)")
            print("Complete the handover FIRST before any other tasks:")
            print("\n1. Get session information:")
            print("   Command: python orchestrate.py handover --summary info")
            print("2. Create comprehensive handover document")
            print("3. Get user approval for handover")
            print("4. Save handover using:")
            print("   cat handover_content | python orchestrate.py handover --summary save")
            orchestration_data["phases"].append("handover_creation")
            
            print("\n" + "="*60)
            print("📋 PHASE 2: MAINTENANCE TASK SELECTION")
            print("="*60)
            
            if not args.no_cleanup:
                print("After handover is complete, present maintenance options:")
                print("\nAvailable maintenance tasks:")
                for i, task in enumerate(task_files, 1):
                    print(f"  {i}. {task.replace('_', ' ').title()}")
                
                print("\nAsk user: 'Would you like to run maintenance checks?'")
                print("If yes, explain you'll go through them one at a time")
                orchestration_data["phases"].append("task_selection")
                
                print("\n" + "="*60)
                print("📋 PHASE 3: MAINTENANCE ANALYSIS (ONE BY ONE)")
                print("="*60)
                print("⚠️ CRITICAL: Process tasks ONE AT A TIME with user review between each!")
                print("\nFor EACH task (starting with first, then asking about next):")
                print("1. Tell user: 'Running [task name] check...'")
                print("2. Launch ONE sub-agent:")
                print("   - Use description: 'Sub-Agent Assignment: (Maintenance) [task name]'")
                print("   - Use Task tool with subagent_type='general-purpose'")
                print("3. Wait for agent to complete and return results")
                print("4. Review findings with user")
                print("5. Make recommendations (safe/risky/optional)")
                print("6. Get user decisions")
                print("7. Execute approved fixes if any")
                print("8. Ask: 'Would you like to run the next check?'")
                print("9. If yes, repeat from step 1 with next task")
                print("\n⚠️ NEVER launch multiple agents before reviewing results!")
                
                for i, task in enumerate(task_files, 1):
                    task_instruction = {
                        "task_number": i,
                        "task_name": task,
                        "mode": "analyze",
                        "agent_template": manager.get_maintenance_agent_path(),
                        "task_document": f"{tasks_path}/{task}.md",
                        "report_path": f"{manager.get_reports_directory()}/findings-{task}-{session_id}.md"
                    }
                    
                    print(f"\n   Task {i}: {task}")
                    print(f"   When running this specific task:")
                    print(f"   Task tool description: 'Sub-Agent Assignment: (Maintenance) {task.replace('_', ' ')}'")
                    print(f"   AGENT_INSTRUCTION_ANALYZE:")
                    print(f"   {json.dumps(task_instruction, indent=6)}")
                    print(f"\n   Task tool prompt should be:")
                    print(f"   'Act as maintenance-agent. Read {task_instruction['agent_template']}")
                    print(f"   Execute task: {task_instruction['task_document']}")
                    print(f"   Mode: ANALYZE. Save findings to: {task_instruction['report_path']}'")
                orchestration_data["phases"].append("maintenance_analysis")
            
            if not args.no_cleanup:
                print("\n" + "="*60)
                print("📋 PHASE 4: REVIEW WITH RECOMMENDATIONS")
                print("="*60)
                print("\n🎯 This happens WITHIN Phase 3 for each task!")
                print("\nWhen reviewing EACH task's findings:")
                print("1. Analyze the findings and categorize:")
                print("   - ✅ Safe to fix (won't break anything)")
                print("   - ⚠️ Needs review (could affect functionality)")
                print("   - 💡 Optional (nice to have)")
                print("2. Present with YOUR recommendations:")
                print("   'Found X issues. Here's my analysis:'")
                print("   - Explain what each finding means")
                print("   - Recommend which to fix")
                print("   - Explain any risks")
                print("3. Get user's specific decisions")
                print("4. Save decisions to JSON if fixes approved")
                
                print("\n⚠️ NEVER:")
                print("  - Present all tasks at once")
                print("  - Show lists of numbers without context")
                print("  - Move to next task before current is complete")
                
                print("\n✅ ALWAYS:")
                print("  - Explain what each finding means")
                print("  - Give user control over each decision")
                print("  - Show exactly what will be done")
                print("  - Report what was actually executed")
                
                orchestration_data["phases"].append("conversational_review")
                orchestration_data["phases"].append("execute_fixes")
            
            print("\n" + "="*60)
            print("📋 PHASE 5: DECISION TRACKING")
            print("="*60)
            print("\nFor EACH task that needs fixes:")
            print("1. Create decision file at:")
            print(f"   {decisions_dir}/decisions_[task_name]_{session_id}.json")
            print("\n2. Decision file format:")
            decision_template = {
                "session_id": session_id,
                "task": "task_name",
                "timestamp": "ISO-8601 timestamp",
                "findings_count": "number",
                "decisions": [
                    {
                        "item": "what was found",
                        "action": "user's decision",
                        "details": "specific instructions"
                    }
                ],
                "approved_by_user": True
            }
            print(json.dumps(decision_template, indent=3))
            
            print("\n3. Launch fix agent with:")
            fix_instruction = {
                "mode": "fix",
                "decisions_file": "path/to/decisions_file.json",
                "original_report": "path/to/findings_report.md"
            }
            print(f"   AGENT_INSTRUCTION_FIX:")
            print(f"   {json.dumps(fix_instruction, indent=6)}")
            
            if not args.no_git:
                print("\n" + "="*60)
                print("📋 PHASE 6: GIT COMMIT")
                print("="*60)
                print("After all fixes are complete:")
                print("1. Show git status")
                print("2. Create meaningful commit message")
                print("3. Get user approval")
                print("4. Commit with approved message")
                orchestration_data["phases"].append("git_commit")
            
            print("\n" + "="*60)
            print("🚀 ORCHESTRATION DATA")
            print("="*60)
            print(json.dumps(orchestration_data, indent=2))
            
            print("\n" + "="*60)
            print("🎬 START EXECUTION NOW")
            print("="*60)
            print("Launch the Task tool commands for Phase 1!")
            print("Remember: User experience is conversational, not automated.")

if __name__ == "__main__":
    main()
