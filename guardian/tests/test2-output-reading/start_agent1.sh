#!/bin/bash

echo "🚀 Starting Agent 1 with Guardian MCP Server"
echo "============================================"

AGENT_DIR="$(cd "$(dirname "$0")/agent1" && pwd)"
MCP_CONFIG="$AGENT_DIR/.claude/settings.json"

echo "📁 Agent workspace: $AGENT_DIR"
echo "🔧 MCP config: $MCP_CONFIG"
echo ""

cd "$AGENT_DIR"

echo "Starting Claude with Guardian MCP server..."
echo "Once Claude starts, tell it: 'Read START_HERE.md and follow the instructions'"
echo ""

claude --dangerously-skip-permissions --mcp-config "$MCP_CONFIG"