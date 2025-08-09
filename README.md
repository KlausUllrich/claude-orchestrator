# Claude Orchestrate Test Project

⚠️ **STATUS: Early Prototype - Components exist but are NOT integrated**

This is a test project for developing the claude-orchestrator tool.

## Project Structure

```
claude-orchestrate/
├── .claude/                  # Claude configuration and hooks
├── Docs/                     # Project documentation
├── Source/                   # Project source code (if any)
├── claude-orchestrator/      # The orchestration tool (portable)
└── .orchestrator/           # Project-specific orchestrator data
```

## Using Claude Orchestrator

The `claude-orchestrator/` folder contains the complete orchestration tool. 
This folder can be copied to any project to add orchestration capabilities.

### Quick Start

```bash
cd claude-orchestrator
./setup.sh --project-type unity
./orchestrate.py status
```

## About This Project

This project is used for developing and testing the claude-orchestrator tool.
In a real project, this README would contain project-specific information.

---

For claude-orchestrator documentation, see [claude-orchestrator/README.md](claude-orchestrator/README.md)
