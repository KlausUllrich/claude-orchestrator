#!/usr/bin/env python3
from pathlib import Path

workspace = Path(".orchestrate/orchestrator_system")
outputs_dir = workspace / "outputs"

for file in outputs_dir.glob("*.txt"):
    file.unlink()
    print(f"🗑️ Cleared: {file.name}")

print("✨ All outputs cleared!")
