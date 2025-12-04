#!/usr/bin/env python3
"""
Organize documentation files into structured folders.

This script moves all documentation from the root folder into organized subdirectories.
"""

import shutil
from pathlib import Path

# Define the organization structure
ORGANIZATION = {
    # Setup and Getting Started
    "docs/setup": [
        "QUICK_START.md",
        "SETUP_OPENAI.md",
        "AWS_SETUP_GUIDE.md",
        "AWS_CREDITS_GUIDE.md",
        "SECURITY_BEST_PRACTICES.md",
        "LLM_AGENTS_QUICKSTART.md",
        "LLM_OPTIONS_COMPARISON.md",
        "MULTI_MODEL_SETUP.md",
    ],
    
    # User Guides
    "docs/guides": [
        "WEB_DASHBOARD_GUIDE.md",
        "ENHANCED_DASHBOARD_GUIDE.md",
        "AGENT_MONITORING_GUIDE.md",
        "AGENT_INTERVIEW_GUIDE.md",
        "AUDIT_PHASE_TRACKER_GUIDE.md",
        "ITERATIVE_AUDIT_IMPROVEMENT_WORKFLOW.md",
    ],
    
    # Audit Methodology
    "docs/audit-methodology": [
        "AUDIT_EXECUTION_PHASES.md",
        "COMPLETE_AUDIT_WORKFLOW_VISION.md",
    ],
    
    # Team and Agent Information
    "docs/team": [
        "TEAM_SYSTEM_PROMPTS_AND_CAPABILITIES.md",
    ],
    
    # Session Notes and Implementation Records
    "docs/session-notes": [
        "SESSION_SUMMARY.md",
        "SESSION_COMPLETE_DASHBOARD_ENHANCEMENT.md",
        "PHASE_TRACKER_IMPLEMENTATION_COMPLETE.md",
        "DASHBOARD_ENHANCEMENT_COMPLETE.md",
        "DASHBOARD_FEATURES_SUMMARY.md",
        "CHUCK_AGENT_COMPLETE.md",
        "CHUCK_KNOWLEDGE_FIX_COMPLETE.md",
        "ALL_AGENTS_DASHBOARD_READY.md",
        "KNOWLEDGE_STRUCTURE_UPDATE.md",
        "REMAINING_AUDITORS_REVIEW.md",
        "SYSTEM_PROMPT_EDITOR_COMPLETE.md",
        "TASKS_5.5_AND_5.6_COMPLETE.md",
    ],
    
    # Archive (old/deprecated docs)
    "docs/archive": [
        "START_HERE_TOMORROW.md",
        "START_HERE_ESTHER.md",
        "WHERE_WE_ARE.md",
        "PIVOT_SUMMARY.md",
        "AGENT_WORKFLOW_SETUP.md",
        "AGENT_KNOWLEDGE_AND_TASKS_DESIGN.md",
        "AGENT_KNOWLEDGE_AND_TASKS_IMPLEMENTATION.md",
        "ESTHER_IMPLEMENTATION_GUIDE.md",
    ],
}

def move_file(source: Path, dest_dir: Path):
    """Move a file to destination directory."""
    if not source.exists():
        print(f"⚠️  File not found: {source}")
        return False
    
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest_file = dest_dir / source.name
    
    try:
        shutil.move(str(source), str(dest_file))
        print(f"✓ Moved {source.name} → {dest_dir}")
        return True
    except Exception as e:
        print(f"✗ Error moving {source.name}: {e}")
        return False

def main():
    """Organize all documentation files."""
    print("=" * 80)
    print("ORGANIZING DOCUMENTATION")
    print("=" * 80)
    print()
    
    moved_count = 0
    not_found_count = 0
    
    for dest_dir, files in ORGANIZATION.items():
        print(f"\n📁 {dest_dir}/")
        for filename in files:
            source = Path(filename)
            if move_file(source, Path(dest_dir)):
                moved_count += 1
            else:
                not_found_count += 1
    
    print()
    print("=" * 80)
    print(f"✓ Moved {moved_count} files")
    if not_found_count > 0:
        print(f"⚠️  {not_found_count} files not found (may have been moved already)")
    print("=" * 80)
    print()
    print("Documentation is now organized in docs/ folder:")
    print("  • docs/setup/          - Setup and installation guides")
    print("  • docs/guides/         - User guides and how-tos")
    print("  • docs/audit-methodology/ - Audit process documentation")
    print("  • docs/team/           - Team and agent information")
    print("  • docs/session-notes/  - Implementation session notes")
    print("  • docs/archive/        - Old/deprecated documentation")
    print()

if __name__ == '__main__':
    main()
