#!/bin/bash

# Monitor MCP database and inject messages into Agent's WezTerm pane
AGENT_ID="${1:-agent1}"
DB_PATH="/home/klaus/game-projects/claude-orchestrate/guardian/mcp-server/db/coordination.db"

echo "[Monitor] Starting MCP monitor for $AGENT_ID"
echo "[Monitor] This script polls the database so the agent doesn't have to"
echo ""

# Keep track of last seen message ID to avoid duplicates
LAST_MESSAGE_ID=0

while true; do
    # Check for new messages for this agent
    NEW_MESSAGES=$(sqlite3 "$DB_PATH" "
        SELECT id, from_agent, content 
        FROM messages 
        WHERE to_agent='$AGENT_ID' 
        AND id > $LAST_MESSAGE_ID
        ORDER BY id ASC;
    " 2>/dev/null)
    
    if [ ! -z "$NEW_MESSAGES" ]; then
        echo "[Monitor] Found new message(s) for $AGENT_ID"
        
        # Update last seen ID
        LAST_MESSAGE_ID=$(sqlite3 "$DB_PATH" "SELECT MAX(id) FROM messages WHERE to_agent='$AGENT_ID';" 2>/dev/null)
        
        # Find the WezTerm pane for this agent
        # Assumes the working directory contains agent1 or agent2
        PANE_ID=$(wezterm cli list | grep "$AGENT_ID" | awk '{print $1}' | head -1)
        
        if [ ! -z "$PANE_ID" ]; then
            echo "[Monitor] Injecting notification into pane $PANE_ID"
            
            # Inject a message into the agent's terminal
            wezterm cli send-text --pane-id "$PANE_ID" \
                "📬 SYSTEM: New MCP message available. Use check_messages tool to read it."
            
            # Send Enter to submit to Claude
            wezterm cli send-text --pane-id "$PANE_ID" $'\n'
        else
            echo "[Monitor] Warning: Could not find WezTerm pane for $AGENT_ID"
        fi
    fi
    
    # Check for new outputs from other agents
    NEW_OUTPUTS=$(sqlite3 "$DB_PATH" "
        SELECT agent_id, file_path 
        FROM outputs 
        WHERE agent_id != '$AGENT_ID'
        AND created_at > datetime('now', '-10 seconds')
        LIMIT 1;
    " 2>/dev/null)
    
    if [ ! -z "$NEW_OUTPUTS" ]; then
        echo "[Monitor] Found new output: $NEW_OUTPUTS"
        
        PANE_ID=$(wezterm cli list | grep "$AGENT_ID" | awk '{print $1}' | head -1)
        if [ ! -z "$PANE_ID" ]; then
            wezterm cli send-text --pane-id "$PANE_ID" \
                "📄 SYSTEM: New output available from another agent: $NEW_OUTPUTS"
            wezterm cli send-text --pane-id "$PANE_ID" $'\n'
        fi
    fi
    
    sleep 2
done