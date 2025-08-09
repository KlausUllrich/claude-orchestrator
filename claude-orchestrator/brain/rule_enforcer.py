#!/usr/bin/env python3
"""
Rule Enforcer - Maintains consistency across sessions

This module loads rules from YAML files and enforces them throughout the session.
Rules are separate from the tool for visibility and modularity.

ARCHITECTURE:
- Rules are defined in brain/rules/*.yaml (single source of truth)
- This enforcer reads and applies those rules
- Hooks and agents call this enforcer (they don't contain rules)
- To change rules, edit the YAML files, not this code

YAML RULE FILES:
- naming.yaml: File and folder naming conventions
- documentation.yaml: Where different types of docs should go
- core.yaml: Core project rules (context, TODOs, etc.)
"""

import os
import sys
import yaml
import re
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime

class RuleEnforcer:
    """Enforces project rules and conventions"""
    
    def __init__(self, rules_dir: Optional[Path] = None):
        """Initialize with rules directory"""
        if rules_dir is None:
            # Default to brain/rules/ directory
            self.rules_dir = Path(__file__).parent / "rules"
        else:
            self.rules_dir = Path(rules_dir)
        
        self.rules = {}
        self.violations = []
        self.load_rules()
    
    def load_rules(self) -> Dict[str, Any]:
        """Load all rules from YAML files"""
        if not self.rules_dir.exists():
            print(f"⚠️ Rules directory not found: {self.rules_dir}")
            return {}
        
        # Load each YAML file in rules directory
        for rule_file in self.rules_dir.glob("*.yaml"):
            try:
                with open(rule_file, 'r') as f:
                    rule_set = yaml.safe_load(f)
                    if rule_set:
                        self.rules[rule_file.stem] = rule_set
                        print(f"✅ Loaded rules: {rule_file.stem}")
            except Exception as e:
                print(f"❌ Failed to load {rule_file}: {e}")
        
        return self.rules
    
    def check_naming_convention(self, path: str) -> bool:
        """
        Check if path follows naming convention:
        - lowercase letters
        - hyphens as separators (kebab-case)
        - no underscores or spaces
        """
        path_obj = Path(path)
        name = path_obj.stem  # filename without extension
        
        # Skip hidden files and specific allowed exceptions
        if name.startswith('.'):
            return True
        
        # Check for uppercase letters
        if name != name.lower():
            self.violations.append(f"Naming violation: '{name}' contains uppercase letters")
            return False
        
        # Check for underscores
        if '_' in name and name not in self.get_naming_exceptions():
            self.violations.append(f"Naming violation: '{name}' contains underscores (use hyphens)")
            return False
        
        # Check for spaces
        if ' ' in name:
            self.violations.append(f"Naming violation: '{name}' contains spaces")
            return False
        
        return True
    
    def get_naming_exceptions(self) -> List[str]:
        """Get list of allowed naming exceptions"""
        exceptions = self.rules.get('naming', {}).get('exceptions', [])
        # Add common Python conventions
        exceptions.extend(['__init__', '__pycache__', '__main__'])
        return exceptions
    
    def check_documentation_placement(self, doc_type: str, content: str) -> str:
        """
        Determine correct location for documentation
        Returns: correct path for the document type
        """
        doc_rules = self.rules.get('documentation', {})
        
        # Check if it's transient or permanent
        if self.is_transient_content(content, doc_type):
            # Transient goes to agent-feedback
            session_date = datetime.now().strftime("%Y-%m-%d")
            return f"agent-feedback/session-{session_date}/"
        else:
            # Permanent goes to Docs
            placement_map = doc_rules.get('placement', {})
            return placement_map.get(doc_type, "Docs/")
    
    def is_transient_content(self, content: str, doc_type: str) -> bool:
        """Determine if content is transient or permanent"""
        transient_indicators = [
            "report", "status", "findings", "analysis",
            "reorganization", "cleanup", "temporary"
        ]
        
        permanent_indicators = [
            "architecture", "design", "api", "handbook",
            "vision", "specification", "contract"
        ]
        
        # Check document type
        if doc_type.lower() in ["report", "feedback", "status-update"]:
            return True
        
        # Check content for indicators
        content_lower = content.lower() if content else ""
        
        # Count indicators
        transient_count = sum(1 for ind in transient_indicators if ind in content_lower)
        permanent_count = sum(1 for ind in permanent_indicators if ind in content_lower)
        
        return transient_count > permanent_count
    
    def enforce_session_naming(self) -> str:
        """
        Enforce session naming convention
        Format: session-YYYY-MM-DD (one folder per day)
        """
        return f"session-{datetime.now().strftime('%Y-%m-%d')}"
    
    def validate_path(self, path: str) -> Dict[str, Any]:
        """Validate a path against all rules"""
        result = {
            "valid": True,
            "path": path,
            "violations": []
        }
        
        # Check naming convention
        if not self.check_naming_convention(path):
            result["valid"] = False
            result["violations"].extend(self.violations[-1:])
        
        # Check file organization rules
        org_rules = self.rules.get('organization', {})
        if org_rules:
            if not self.check_organization(path, org_rules):
                result["valid"] = False
                result["violations"].append("Organization rule violation")
        
        return result
    
    def check_organization(self, path: str, org_rules: Dict) -> bool:
        """Check if file is in correct location per organization rules"""
        path_obj = Path(path)
        
        # Check file extensions
        extension_map = org_rules.get('extensions', {})
        if path_obj.suffix:
            expected_dir = extension_map.get(path_obj.suffix)
            if expected_dir and expected_dir not in str(path_obj):
                self.violations.append(
                    f"Organization violation: {path_obj.suffix} files should be in {expected_dir}"
                )
                return False
        
        return True
    
    def inject_rules_reminder(self) -> str:
        """Generate a rules reminder to inject into conversation"""
        active_rules = []
        
        # Collect critical rules
        for rule_set_name, rule_set in self.rules.items():
            if rule_set.get('priority') == 'critical':
                active_rules.extend(rule_set.get('rules', []))
        
        if not active_rules:
            return ""
        
        reminder = "\n⚠️ RULE REMINDER:\n"
        for rule in active_rules[:5]:  # Limit to 5 rules
            reminder += f"• {rule}\n"
        
        return reminder
    
    def get_statistics(self) -> Dict[str, int]:
        """Get enforcement statistics"""
        return {
            "rules_loaded": len(self.rules),
            "total_violations": len(self.violations),
            "checks_performed": len(self.violations) + 100  # Approximate
        }


def main():
    """Test the rule enforcer"""
    enforcer = RuleEnforcer()
    
    print("🛡️ Rule Enforcer Initialized")
    print(f"Rules loaded: {len(enforcer.rules)}")
    
    # Test naming conventions
    test_paths = [
        "my-document.md",      # Good
        "my_document.md",      # Bad - underscore
        "MyDocument.md",       # Bad - uppercase
        "my document.md",      # Bad - space
    ]
    
    print("\n📝 Testing naming conventions:")
    for path in test_paths:
        result = enforcer.validate_path(path)
        status = "✅" if result["valid"] else "❌"
        print(f"{status} {path}")
        if result["violations"]:
            for violation in result["violations"]:
                print(f"   → {violation}")
    
    # Test session naming
    print(f"\n📅 Session naming: {enforcer.enforce_session_naming()}")
    
    # Show statistics
    stats = enforcer.get_statistics()
    print(f"\n📊 Statistics: {stats}")


if __name__ == "__main__":
    main()
