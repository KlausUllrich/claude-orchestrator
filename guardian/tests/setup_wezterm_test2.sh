#!/bin/bash

echo "🚀 Setting up Test 2 in WezTerm"
echo "================================"

GUARDIAN_DIR="/home/klaus/game-projects/claude-orchestrate/guardian"
TEST_DIR="$GUARDIAN_DIR/tests/test2-output-reading"

# Create database if it doesn't exist
echo "Initializing database..."
cd "$GUARDIAN_DIR/mcp-server"
if [ ! -f "db/coordination.db" ]; then
    mkdir -p db
    sqlite3 db/coordination.db < /dev/null
    echo "Database created"
fi

echo ""
echo "📋 Manual Setup Instructions:"
echo ""
echo "1. Open WezTerm"
echo ""
echo "2. Create first pane for Agent 1:"
echo "   cd $TEST_DIR/agent1"
echo "   claude --dangerously-skip-permissions --mcp-config .claude/settings.json"
echo "   # Tell Claude: 'Read START_HERE.md and follow the instructions'"
echo ""
echo "3. Split pane (Ctrl+Shift+% for vertical split)"
echo ""
echo "4. In second pane for Agent 2:"
echo "   cd $TEST_DIR/agent2"
echo "   claude --dangerously-skip-permissions --mcp-config .claude/settings.json"
echo "   # Tell Claude: 'Read START_HERE.md and follow the instructions'"
echo ""
echo "5. Optional: Create third pane to monitor database:"
echo "   watch -n 1 'sqlite3 $GUARDIAN_DIR/mcp-server/db/coordination.db \"SELECT * FROM agents; SELECT * FROM messages ORDER BY created_at DESC LIMIT 5; SELECT * FROM outputs ORDER BY created_at DESC LIMIT 5;\"'"
echo ""
echo "Expected behavior:"
echo "- Agent 2 will analyze webpage and create output"
echo "- Agent 2 will notify via MCP that output is ready"
echo "- Agent 1 should detect and read the output (this is the challenge!)"