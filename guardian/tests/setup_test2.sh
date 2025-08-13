#!/bin/bash

# Test 2: Output Reading Pattern Setup Script
# Agent 2 creates webpage summary → Agent 1 reads output

echo "🚀 Setting up Test 2: Output Reading Pattern"
echo "==========================================="

# Get the guardian directory path
GUARDIAN_DIR="$(cd "$(dirname "$0")/.." && pwd)"
TEST_DIR="$GUARDIAN_DIR/tests/test2-output-reading"

echo "📁 Creating test workspace at: $TEST_DIR"

# Clean up any previous test
rm -rf "$TEST_DIR"

# Create agent directories
mkdir -p "$TEST_DIR/agent1/outputs"
mkdir -p "$TEST_DIR/agent1/.claude"
mkdir -p "$TEST_DIR/agent2/outputs"
mkdir -p "$TEST_DIR/agent2/.claude"

echo "📝 Creating MCP configuration files..."

# Create Agent 1 MCP config
cat > "$TEST_DIR/agent1/.claude/settings.json" << EOF
{
  "mcpServers": {
    "guardian": {
      "command": "node",
      "args": ["$GUARDIAN_DIR/mcp-server/server.js"]
    }
  }
}
EOF

# Create Agent 2 MCP config
cat > "$TEST_DIR/agent2/.claude/settings.json" << EOF
{
  "mcpServers": {
    "guardian": {
      "command": "node",
      "args": ["$GUARDIAN_DIR/mcp-server/server.js"]
    }
  }
}
EOF

echo "📋 Creating agent instruction files..."

# Create Agent 1 instructions (Reader)
cat > "$TEST_DIR/agent1/START_HERE.md" << 'EOF'
# Agent 1: Output Reader

You are Agent 1, responsible for reading outputs from Agent 2.

## Your Task

1. First, register yourself with the Guardian MCP server:
   - Use `register_agent` tool with:
     - agent_id: "agent1"
     - workspace_path: (current directory path)

2. Update your status to show you're waiting:
   - Use `update_status` tool with status "waiting" and details "Waiting for Agent 2 output"

3. Wait for Agent 2 to produce output:
   - Use `wait_for_output` tool with:
     - waiting_agent: "agent1"
     - from_agent: "agent2"
     - timeout_ms: 60000 (1 minute)

4. When output is available:
   - Read the file that Agent 2 created
   - Summarize what you found in the file
   - Update your status to "complete"

## Important
- Do NOT poll or repeatedly check - the MCP server will notify you
- The Guardian system uses event-driven notifications
- Trust the wait_for_output tool to tell you when the file is ready

## Success Criteria
- Successfully receive notification about Agent 2's output
- Read and summarize the webpage analysis created by Agent 2
- No polling loops used
EOF

# Create Agent 2 instructions (Writer)
cat > "$TEST_DIR/agent2/START_HERE.md" << 'EOF'
# Agent 2: Webpage Analyzer

You are Agent 2, responsible for analyzing a webpage and creating output for Agent 1.

## Your Task

1. First, register yourself with the Guardian MCP server:
   - Use `register_agent` tool with:
     - agent_id: "agent2"
     - workspace_path: (current directory path)

2. Update your status to "busy":
   - Use `update_status` with details "Analyzing webpage"

3. Analyze the following webpage: https://www.anthropic.com
   - Use WebFetch to get the page content
   - Extract key information:
     - Main heading
     - Key products/services mentioned
     - Number of main navigation items
     - Primary call-to-action

4. Create output file:
   - Write your analysis to `outputs/webpage_analysis.txt`
   - Include:
     - Timestamp of analysis
     - URL analyzed
     - Your findings in a structured format

5. Notify the system that your output is ready:
   - Use `notify_output_ready` tool with:
     - agent_id: "agent2"
     - file_path: (full path to your output file)
     - metadata: { "url": "https://www.anthropic.com", "type": "webpage_analysis" }

6. Update status to "complete"

## Important
- Create a clear, readable analysis file
- Use the notify_output_ready tool - this triggers the event system
- Do NOT directly message Agent 1 - let the Guardian handle coordination

## Success Criteria
- Successfully analyze the webpage
- Create a well-formatted output file
- Trigger the notification system properly
EOF

echo "📚 Creating test documentation..."

cat > "$TEST_DIR/README.md" << EOF
# Test 2: Output Reading Pattern

## Objective
Demonstrate event-driven communication between agents using the Guardian MCP server.
Agent 2 creates output, Agent 1 automatically receives notification and reads it.

## Architecture
- Guardian MCP server provides coordination
- File monitoring detects new outputs
- Event-driven notifications (no polling)
- SQLite message queue for reliability

## How to Run

### Step 1: Install dependencies (if not done)
\`\`\`bash
cd $GUARDIAN_DIR/mcp-server
npm install
\`\`\`

### Step 2: Start Agent 2 (Writer) FIRST
\`\`\`bash
cd $TEST_DIR/agent2
claude --dangerously-skip-permissions
# Read START_HERE.md and follow instructions
\`\`\`

### Step 3: Start Agent 1 (Reader) in another terminal
\`\`\`bash
cd $TEST_DIR/agent1
claude --dangerously-skip-permissions
# Read START_HERE.md and follow instructions
\`\`\`

### Step 4: Observe
- Agent 2 will create webpage analysis
- Guardian detects the new file
- Agent 1 receives notification instantly
- No polling required!

## Expected Outcome
- Agent 2 creates \`outputs/webpage_analysis.txt\`
- Agent 1 receives notification via MCP
- Agent 1 reads and summarizes the analysis
- All communication logged in Guardian database

## Verification
Check the Guardian database:
\`\`\`bash
sqlite3 $GUARDIAN_DIR/mcp-server/db/coordination.db
.tables
SELECT * FROM messages;
SELECT * FROM outputs;
\`\`\`
EOF

echo ""
echo "✅ Test 2 setup complete!"
echo ""
echo "📖 Next steps:"
echo "1. Install MCP server dependencies:"
echo "   cd $GUARDIAN_DIR/mcp-server && npm install"
echo ""
echo "2. Open 2 terminal windows in WezTerm"
echo ""
echo "3. Start Agent 2 (writer) first:"
echo "   cd $TEST_DIR/agent2"
echo "   claude --dangerously-skip-permissions"
echo ""
echo "4. Start Agent 1 (reader) in second terminal:"
echo "   cd $TEST_DIR/agent1"
echo "   claude --dangerously-skip-permissions"
echo ""
echo "5. Watch the event-driven magic happen! 🎉"