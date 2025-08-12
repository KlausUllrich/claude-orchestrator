#!/bin/bash
# Start the Claude Orchestrator System

echo "========================================"
echo "🎭 CLAUDE ORCHESTRATOR SYSTEM"
echo "========================================"
echo ""
echo "Launching orchestrator Claude with 3 sub-agents capability..."
echo ""
echo "The orchestrator can:"
echo "  • Launch tasks on 3 sub-agents"
echo "  • Run them in parallel or sequence"
echo "  • Share context between agents"
echo "  • Monitor their status"
echo "  • Read their outputs"
echo ""
echo "Example commands to give the orchestrator:"
echo '  "Check the status of all agents"'
echo '  "Launch agent1 with task: analyze this codebase"'
echo '  "Run all 3 agents in parallel with different tasks"'
echo '  "Read the output from agent2"'
echo ""
echo "========================================"
echo ""

# Launch Claude with orchestrator configuration
claude --append-system-prompt "You are the Master Orchestrator Claude managing 3 sub-agent Claudes. 

IMPORTANT: First, use the Read tool to read .orchestrate/orchestrator_system/ORCHESTRATOR_README.md for your complete instructions.

You have these key commands:
- Check status: python .orchestrate/orchestrator_system/agents/check_status.py
- Launch single: python .orchestrate/orchestrator_system/agents/launch_agent.py agent1 'task'
- Launch parallel: python .orchestrate/orchestrator_system/agents/launch_parallel.py 'task1' 'task2' 'task3'
- Read output: cat .orchestrate/orchestrator_system/outputs/agent1_latest.txt

Start by reading your full instructions, then help the user coordinate tasks across your 3 sub-agents."