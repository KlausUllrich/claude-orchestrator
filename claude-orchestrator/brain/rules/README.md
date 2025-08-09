# Rule System - Single Source of Truth

## 📍 How This Works

This folder contains **ALL project rules** in YAML format.
These files are the **single source of truth** - edit them to change rules.

## 📂 Rule Files

- **naming.yaml** - File and folder naming conventions
- **documentation.yaml** - Where different types of docs go  
- **core.yaml** - Core project rules (context, TODOs, etc.)

## 🔄 Architecture

```
1. Rules defined here (YAML files)
   ↓
2. RuleEnforcer reads these files
   ↓
3. Hooks/Agents call RuleEnforcer
   ↓
4. Rules are applied consistently
```

## ✏️ How to Change Rules

1. Edit the YAML file for the rule you want to change
2. Save the file
3. Rules are automatically reloaded next time they're checked
4. No code changes needed!

## 📝 YAML Structure

Each rule file has:
```yaml
priority: critical|high|medium|low
description: What this rule set does
rules:
  - List of rules
  - Another rule
```

## 🎯 Key Principle

**Never duplicate rules in code!**
- ❌ Don't hardcode rules in hooks
- ❌ Don't copy rules into agents
- ✅ Always read from these YAML files
- ✅ This ensures consistency everywhere

## 📚 Example Usage

```python
from brain.rule_enforcer import RuleEnforcer

# This loads all rules from this folder
enforcer = RuleEnforcer()

# Check a naming convention (reads naming.yaml)
if enforcer.check_naming_convention("my-file.md"):
    print("Valid name!")

# Get session folder (reads documentation.yaml)
session = enforcer.enforce_session_naming()
```

---
*To understand or modify project rules, look at the YAML files in this folder.*
*They are the single source of truth for all project conventions.*
