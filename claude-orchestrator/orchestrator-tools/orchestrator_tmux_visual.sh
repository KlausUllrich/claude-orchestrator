#!/bin/bash
# Visual Orchestrator System with Tmux
# 4 panes: 1 orchestrator + 3 agents

SESSION="orchestrator_visual"

# Kill existing session
tmux kill-session -t $SESSION 2>/dev/null

# Create new session with orchestrator
tmux new-session -d -s $SESSION -n "Orchestrator System"

# Create 2x2 grid
tmux split-window -h
tmux split-window -v
tmux select-pane -t 0
tmux split-window -v

# Pane 0: Main Orchestrator
tmux send-keys -t 0 "clear" C-m
tmux send-keys -t 0 'echo -e "\\033[1;36m═══════════════════════════════════════\\033[0m"' C-m
tmux send-keys -t 0 'echo -e "\\033[1;36m    🎭 MASTER ORCHESTRATOR\\033[0m"' C-m
tmux send-keys -t 0 'echo -e "\\033[1;36m═══════════════════════════════════════\\033[0m"' C-m
tmux send-keys -t 0 'echo ""' C-m
tmux send-keys -t 0 'echo "Commands:"' C-m
tmux send-keys -t 0 'echo "  check    - Check all agents status"' C-m
tmux send-keys -t 0 'echo "  launch N - Launch agent N with task"' C-m
tmux send-keys -t 0 'echo "  parallel - Launch all 3 agents"' C-m
tmux send-keys -t 0 'echo "  read N   - Read agent N output"' C-m
tmux send-keys -t 0 'echo ""' C-m
tmux send-keys -t 0 'echo "Starting orchestrator Claude..."' C-m
tmux send-keys -t 0 'echo ""' C-m

# Start the orchestrator
tmux send-keys -t 0 'claude --append-system-prompt "You are the Master Orchestrator managing 3 agents. Commands: python .orchestrate/orchestrator_system/agents/check_status.py for status, python .orchestrate/orchestrator_system/agents/launch_agent.py agentN task for single launch, python .orchestrate/orchestrator_system/agents/launch_parallel.py task1 task2 task3 for parallel. Read outputs from .orchestrate/orchestrator_system/outputs/"' C-m

# Pane 1: Agent 1 Monitor
tmux send-keys -t 1 "clear" C-m
tmux send-keys -t 1 'echo -e "\\033[1;32m═══════════════════════════════════════\\033[0m"' C-m
tmux send-keys -t 1 'echo -e "\\033[1;32m    🤖 AGENT 1 MONITOR\\033[0m"' C-m
tmux send-keys -t 1 'echo -e "\\033[1;32m═══════════════════════════════════════\\033[0m"' C-m
tmux send-keys -t 1 'watch -n 2 "echo Agent 1 Status:; echo; cat .orchestrate/orchestrator_system/status/agent1.json 2>/dev/null | python3 -m json.tool || echo Ready; echo; echo Latest Output:; echo; tail -10 .orchestrate/orchestrator_system/outputs/agent1_latest.txt 2>/dev/null || echo No output yet"' C-m

# Pane 2: Agent 2 Monitor
tmux send-keys -t 2 "clear" C-m
tmux send-keys -t 2 'echo -e "\\033[1;33m═══════════════════════════════════════\\033[0m"' C-m
tmux send-keys -t 2 'echo -e "\\033[1;33m    🤖 AGENT 2 MONITOR\\033[0m"' C-m
tmux send-keys -t 2 'echo -e "\\033[1;33m═══════════════════════════════════════\\033[0m"' C-m
tmux send-keys -t 2 'watch -n 2 "echo Agent 2 Status:; echo; cat .orchestrate/orchestrator_system/status/agent2.json 2>/dev/null | python3 -m json.tool || echo Ready; echo; echo Latest Output:; echo; tail -10 .orchestrate/orchestrator_system/outputs/agent2_latest.txt 2>/dev/null || echo No output yet"' C-m

# Pane 3: Agent 3 Monitor
tmux send-keys -t 3 "clear" C-m
tmux send-keys -t 3 'echo -e "\\033[1;35m═══════════════════════════════════════\\033[0m"' C-m
tmux send-keys -t 3 'echo -e "\\033[1;35m    🤖 AGENT 3 MONITOR\\033[0m"' C-m
tmux send-keys -t 3 'echo -e "\\033[1;35m═══════════════════════════════════════\\033[0m"' C-m
tmux send-keys -t 3 'watch -n 2 "echo Agent 3 Status:; echo; cat .orchestrate/orchestrator_system/status/agent3.json 2>/dev/null | python3 -m json.tool || echo Ready; echo; echo Latest Output:; echo; tail -10 .orchestrate/orchestrator_system/outputs/agent3_latest.txt 2>/dev/null || echo No output yet"' C-m

# Attach to session
echo "═══════════════════════════════════════"
echo "   VISUAL ORCHESTRATOR SYSTEM"
echo "═══════════════════════════════════════"
echo ""
echo "Layout:"
echo "  ┌─────────────┬─────────────┐"
echo "  │ ORCHESTRATOR│   AGENT 1   │"
echo "  │  (You talk  │  (Monitor)  │"
echo "  │   to this)  │             │"
echo "  ├─────────────┼─────────────┤"
echo "  │   AGENT 2   │   AGENT 3   │"
echo "  │  (Monitor)  │  (Monitor)  │"
echo "  └─────────────┴─────────────┘"
echo ""
echo "Navigation:"
echo "  Ctrl+B then ↑↓←→  Move between panes"
echo "  Ctrl+B then D     Detach (keep running)"
echo "  Ctrl+B then X     Kill current pane"
echo ""
echo "In the Orchestrator pane, tell Claude:"
echo '  "Launch agent1 to analyze our code"'
echo '  "Run all 3 agents with different tasks"'
echo '  "Check the status of all agents"'
echo ""
echo "═══════════════════════════════════════"

tmux attach-session -t $SESSION