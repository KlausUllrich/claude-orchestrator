#!/bin/bash
# Guardian Tmux Dashboard - Launch multiple Claude agents with live visibility

# Configuration
SESSION_NAME="claude_guardian"
AGENTS=(
    "Analyze the project structure and list main components"
    "Check for code style issues and suggest improvements"
    "Identify potential bugs or edge cases"
    "Write unit test suggestions"
)

# Colors for different panes
COLORS=(blue green yellow magenta)

# Kill existing session if it exists
tmux kill-session -t $SESSION_NAME 2>/dev/null

# Create new session
echo "Creating tmux session: $SESSION_NAME"
tmux new-session -d -s $SESSION_NAME

# Rename window
tmux rename-window -t $SESSION_NAME 'Claude Agents'

# Create 2x2 grid layout
tmux split-window -h -t $SESSION_NAME
tmux split-window -v -t $SESSION_NAME:0.0
tmux split-window -v -t $SESSION_NAME:0.2

# Optional: Add status pane at bottom
tmux select-pane -t $SESSION_NAME:0.0
tmux split-window -v -p 20 -t $SESSION_NAME
tmux send-keys -t $SESSION_NAME:0.4 'echo "=== Guardian Status Panel ==="; watch -n 1 "date; echo; ps aux | grep claude | grep -v grep | wc -l | xargs echo Claude processes:; echo; ls -la agent*.txt 2>/dev/null || echo No output files yet"' C-m

# Launch Claude agents in each pane
for i in {0..3}; do
    PANE_ID=$i
    TASK="${AGENTS[$i]}"
    COLOR="${COLORS[$i]}"
    
    # Add colored header and launch command
    tmux send-keys -t $SESSION_NAME:0.$PANE_ID "clear" C-m
    tmux send-keys -t $SESSION_NAME:0.$PANE_ID "echo -e '\\033[1;34m=== AGENT $((i+1)) ===\\033[0m'" C-m
    tmux send-keys -t $SESSION_NAME:0.$PANE_ID "echo 'Task: $TASK'" C-m
    tmux send-keys -t $SESSION_NAME:0.$PANE_ID "echo '-------------------'" C-m
    tmux send-keys -t $SESSION_NAME:0.$PANE_ID "claude -p \"$TASK\" | tee agent$((i+1))_output.txt" C-m
done

# Attach to session
echo "Attaching to tmux session..."
echo "Use Ctrl+B then arrow keys to navigate between panes"
echo "Use Ctrl+B then D to detach from session"
echo "Use 'tmux attach -t $SESSION_NAME' to reattach"
tmux attach-session -t $SESSION_NAME