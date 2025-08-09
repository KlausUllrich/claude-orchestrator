#!/bin/bash

# Claude Orchestrator Setup Script

echo "🚀 Claude Orchestrator Setup"
echo "============================"

# Parse arguments
PROJECT_TYPE=""
ANALYZE=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --project-type)
            PROJECT_TYPE="$2"
            shift 2
            ;;
        --analyze-project)
            ANALYZE=true
            shift
            ;;
        --help)
            echo "Usage: ./setup.sh [options]"
            echo "Options:"
            echo "  --project-type TYPE    Set project type (unity, love2d, web)"
            echo "  --analyze-project      Analyze existing project structure"
            echo "  --help                 Show this help message"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

# Check Python version
if command -v python3 &>/dev/null; then
    python_version=$(python3 --version 2>&1 | grep -oP '\d+\.\d+')
    echo "✅ Python $python_version found"
else
    echo "❌ Python 3 not found. Please install Python 3.8 or higher."
    exit 1
fi

# Ensure we're in the claude-orchestrator directory (tool directory)
if [ ! -f "setup.sh" ] || [ ! -d "brain" ]; then
    echo "❌ Please run this script from the claude-orchestrator directory"
    exit 1
fi

# Create necessary directories if they don't exist
echo "📁 Ensuring directory structure..."
mkdir -p brain
mkdir -p short-term-memory
mkdir -p long-term-memory/vector_store
mkdir -p workflows/{game-dev,web-dev,love2d,unity}
mkdir -p resource-library/{hooks,agents,documents,project-types}
mkdir -p resource-library/hooks/{session_start,context_guard,rule_enforce,session_end}
mkdir -p resource-library/agents/{doc_maintainer,bug_hunter,code_reviewer,unity_specialist}
mkdir -p resource-library/documents/{handovers,architecture,status}
mkdir -p resource-library/project-types/{unity,love2d,web}
mkdir -p tools
mkdir -p bridges
mkdir -p config
mkdir -p development

# Create project-specific orchestrator directory
echo "📂 Setting up project-specific data directory..."
mkdir -p ../.orchestrator/{state,memory}
mkdir -p ../.orchestrator/state/checkpoints

# Create default configuration if it doesn't exist
if [ ! -f "config/defaults.yaml" ]; then
    echo "📝 Creating default configuration..."
    cat > config/defaults.yaml << 'EOF'
# Claude Orchestrator Default Configuration
context:
  max_tokens: 200000
  warning_levels: [70, 80, 90]
  checkpoint_level: 80

memory:
  short_term_db: "short-term-memory/session_state.db"
  long_term_db: "long-term-memory/knowledge_base.db"
  
monitoring:
  enabled: true
  interval: 60  # seconds

project_types:
  - unity
  - love2d
  - web
EOF
fi

# Set up project type if specified
if [ -n "$PROJECT_TYPE" ]; then
    echo "🎮 Configuring for $PROJECT_TYPE project..."
    echo "project_type: $PROJECT_TYPE" > ../.orchestrator/config.yaml
    
    # Create symlink to active workflow
    ln -sfn "$PROJECT_TYPE" workflows/active
    echo "✅ Activated $PROJECT_TYPE workflow"
fi

# Test the Context Guardian
echo ""
echo "🧪 Testing Context Guardian..."
if python3 tools/context_guardian.py --status; then
    echo "✅ Context Guardian is working"
else
    echo "⚠️ Context Guardian test failed"
fi

# Set up .claude directory hooks (if it exists)
if [ -d "../.claude" ]; then
    echo "🔗 Found .claude directory, ready to link hooks when needed"
    echo "   Use: ./orchestrate.py enable hook <hook-name>"
else
    echo "📝 No .claude directory found. Will create when hooks are enabled."
fi

echo ""
echo "============================"
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "  1. Start monitoring:     python3 tools/context_guardian.py --watch"
echo "  2. Check status:         python3 tools/context_guardian.py --status"
echo "  3. View documentation:   cat development/ARCHITECTURE.md"
echo ""
if [ -z "$PROJECT_TYPE" ]; then
    echo "💡 Tip: Re-run with --project-type to configure for your project:"
    echo "   ./setup.sh --project-type unity"
fi
