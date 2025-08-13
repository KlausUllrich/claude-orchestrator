#!/bin/bash

# Setup proper agent folders with full Claude capabilities
# Only Agent 1 gets the task, others just know how to communicate

echo "=========================================="
echo "AGENT WORKSPACE SETUP"
echo "3 agents with full tools, only protocol knowledge"
echo "=========================================="
echo ""

BASE_DIR="/home/klaus/game-projects/claude-orchestrate/claude-orchestrator/orchestrator-tools/tests"

# Clean and create directories
rm -rf "$BASE_DIR/agent1" "$BASE_DIR/agent2" "$BASE_DIR/agent3"

for i in 1 2 3; do
    AGENT_DIR="$BASE_DIR/agent$i"
    
    echo "Setting up Agent $i workspace..."
    
    # Create directory structure
    mkdir -p "$AGENT_DIR/.claude"
    mkdir -p "$AGENT_DIR/outputs"
    mkdir -p "$AGENT_DIR/inputs"
    
    echo "  ✓ Created $AGENT_DIR"
done

# Agent 1: Gets the actual task
cat > "$BASE_DIR/agent1/protocol.md" << 'EOF'
# Agent 1 - Communication Protocol

You are Agent 1. You have full Claude tool access.

## Communication Channels:
- Your outputs: outputs/
- Agent 2's outputs: ../agent2/outputs/
- Agent 3's outputs: ../agent3/outputs/

## How to communicate with Agent 2:
- Write requests to: ../agent2/inputs/request_from_agent1.txt
- Read responses from: ../agent2/outputs/response_to_agent1.txt

## Available Tools:
You have full access to Read, Write, Bash, and all other Claude tools.

## Waiting for your task...
You will be given a specific task. Use the other agents as needed to complete it.
EOF

# Agent 2: Only knows how to communicate
cat > "$BASE_DIR/agent2/protocol.md" << 'EOF'
# Agent 2 - Communication Protocol

You are Agent 2. You have full Claude tool access.

## Communication Channels:
- Your inputs: inputs/
- Your outputs: outputs/
- Agent 1's outputs: ../agent1/outputs/
- Agent 3's outputs: ../agent3/outputs/

## Protocol:
- Monitor inputs/ for requests
- When you receive a request from Agent 1 (inputs/request_from_agent1.txt):
  - Read and understand it
  - If it requires Agent 3, write to: ../agent3/inputs/request_from_agent2.txt
  - Read Agent 3's response from: ../agent3/outputs/response_to_agent2.txt
  - Report back to Agent 1 via: outputs/response_to_agent1.txt

## Available Tools:
You have full access to Read, Write, Bash, and all other Claude tools.

## Status:
Waiting for requests... Monitor your inputs/ directory.
EOF

# Agent 3: Only knows how to communicate
cat > "$BASE_DIR/agent3/protocol.md" << 'EOF'
# Agent 3 - Communication Protocol

You are Agent 3. You have full Claude tool access.

## Communication Channels:
- Your inputs: inputs/
- Your outputs: outputs/

## Protocol:
- Monitor inputs/ for requests
- When you receive a request from Agent 2 (inputs/request_from_agent2.txt):
  - Read and understand it
  - Process the request
  - Write response to: outputs/response_to_agent2.txt

## Available Tools:
You have full access to Read, Write, Bash, and all other Claude tools.

## Status:
Waiting for requests... Monitor your inputs/ directory.
EOF

# Create the TASK file only for Agent 1
cat > "$BASE_DIR/agent1/TASK.md" << 'EOF'
# TASK FOR AGENT 1 ONLY

## Your Mission:
Get a random number from Agent 3 through Agent 2, then double it.

## Steps:
1. Ask Agent 2 to get a random number from Agent 3
2. Wait for Agent 2's response
3. Double the number
4. Output: "FINAL_RESULT: Original was [X], doubled is [2X]"

## Remember:
- Use the communication protocol described in protocol.md
- Agent 2 doesn't know what to do until you tell them
- Agent 3 doesn't know what to do until Agent 2 tells them

Begin by writing a request to Agent 2.
EOF

echo ""
echo "=========================================="
echo "SETUP COMPLETE!"
echo "=========================================="
echo ""
echo "Three agent workspaces created with:"
echo ""
echo "Agent 1:"
echo "  - protocol.md (how to communicate)"
echo "  - TASK.md (the actual mission)"
echo ""
echo "Agent 2:"
echo "  - protocol.md (how to communicate only)"
echo ""
echo "Agent 3:"
echo "  - protocol.md (how to communicate only)"
echo ""
echo "TO RUN THE TEST:"
echo "================"
echo ""
echo "1. Open 3 terminals/WezTerm panes"
echo ""
echo "2. Terminal 1:"
echo "   cd $BASE_DIR/agent1"
echo "   claude"
echo "   # Then tell Claude to read protocol.md and TASK.md"
echo ""
echo "3. Terminal 2:"
echo "   cd $BASE_DIR/agent2"
echo "   claude"
echo "   # Then tell Claude to read protocol.md and start monitoring"
echo ""
echo "4. Terminal 3:"
echo "   cd $BASE_DIR/agent3"
echo "   claude"
echo "   # Then tell Claude to read protocol.md and start monitoring"
echo ""
echo "Watch as Agent 1 initiates the chain!"